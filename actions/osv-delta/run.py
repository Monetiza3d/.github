#!/usr/bin/env python3
"""Run OSV-Scanner against base/head while keeping scanner output out of CI logs."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


VERSION = "2.7.0"
URL = f"https://github.com/google/osv-scanner/releases/download/v{VERSION}/osv-scanner_linux_amd64"
SHA256 = "160c6253e2922e9e0a6a9771c5c4c40a4b3c6090b34a3cdd5e80c96cc2e4218b"


def download_scanner(destination: Path) -> None:
    request = urllib.request.Request(URL, headers={"User-Agent": "Monetiza3d-OSV-Gate"})
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as target:
        shutil.copyfileobj(response, target)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    if digest != SHA256:
        raise RuntimeError("OSV-Scanner checksum mismatch")
    destination.chmod(0o755)


def scan(binary: Path, directory: Path, output: Path) -> tuple[int, dict]:
    result = subprocess.run(
        [str(binary), "scan", "source", "--recursive", "--format", "json", str(directory)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output.write_text(result.stdout)
    if not result.stdout.strip():
        if "No package sources found" in result.stderr:
            output.write_text('{"results": []}\n')
            return 0, {"results": []}
        raise RuntimeError("OSV-Scanner produced no report")
    import json

    return result.returncode, json.loads(result.stdout)


def findings(report: dict, root: Path) -> dict[tuple[str, str, str, str, str], float | None]:
    detected: dict[tuple[str, str, str, str, str], float | None] = {}
    for result in report.get("results", []):
        source_path = Path(result.get("source", {}).get("path", ""))
        try:
            source = source_path.resolve().relative_to(root.resolve()).as_posix()
        except (OSError, ValueError):
            source = os.path.normpath(str(source_path))
        for package_result in result.get("packages", []):
            package = package_result.get("package", {})
            for vulnerability in package_result.get("vulnerabilities", []):
                aliases = vulnerability.get("aliases", [])
                identifier = sorted([vulnerability.get("id", ""), *aliases])[0]
                severity = vulnerability.get("database_specific", {}).get("severity")
                score: float | None = None
                if isinstance(severity, str):
                    normalized = severity.upper()
                    score = {"CRITICAL": 9.0, "HIGH": 7.0, "MEDIUM": 4.0, "LOW": 0.1}.get(normalized)
                if score is None:
                    for item in vulnerability.get("severity", []):
                        raw = item.get("score", "")
                        try:
                            score = float(raw)
                            break
                        except (TypeError, ValueError):
                            score = cvss_v3_score(raw)
                            if score is not None:
                                break
                key = (
                    identifier,
                    package.get("ecosystem", ""),
                    package.get("name", ""),
                    package.get("version", ""),
                    source,
                )
                detected[key] = score
    return detected


def cvss_v3_score(vector: str) -> float | None:
    """Calculate a CVSS v3.0/v3.1 base score from an OSV vector string."""
    if not vector.startswith(("CVSS:3.0/", "CVSS:3.1/")):
        return None
    metrics = dict(
        pair.split(":", 1)
        for pair in vector.split("/")[1:]
        if ":" in pair
    )
    weights = {
        "AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2},
        "AC": {"L": 0.77, "H": 0.44},
        "UI": {"N": 0.85, "R": 0.62},
        "C": {"H": 0.56, "L": 0.22, "N": 0.0},
        "I": {"H": 0.56, "L": 0.22, "N": 0.0},
        "A": {"H": 0.56, "L": 0.22, "N": 0.0},
    }
    try:
        scope = metrics["S"]
        privilege = (
            {"N": 0.85, "L": 0.62, "H": 0.27}
            if scope == "U"
            else {"N": 0.85, "L": 0.68, "H": 0.5}
        )[metrics["PR"]]
        exploitability = (
            8.22
            * weights["AV"][metrics["AV"]]
            * weights["AC"][metrics["AC"]]
            * privilege
            * weights["UI"][metrics["UI"]]
        )
        impact_sub = 1 - (
            (1 - weights["C"][metrics["C"]])
            * (1 - weights["I"][metrics["I"]])
            * (1 - weights["A"][metrics["A"]])
        )
        if impact_sub <= 0:
            return 0.0
        if scope == "U":
            impact = 6.42 * impact_sub
            base = min(impact + exploitability, 10.0)
        else:
            impact = 7.52 * (impact_sub - 0.029) - 3.25 * (impact_sub - 0.02) ** 15
            base = min(1.08 * (impact + exploitability), 10.0)
        return __import__("math").ceil(base * 10 - 1e-9) / 10
    except (KeyError, ValueError):
        return None


def level(score: float | None) -> str:
    if score is None:
        return "unknown"
    if score >= 9.0:
        return "critical"
    if score >= 7.0:
        return "high"
    return "lower"


def archive_base(base_sha: str, destination: Path) -> None:
    archive_path = destination.parent / "base.tar"
    subprocess.run(
        ["git", "archive", "--format=tar", "--output", str(archive_path), base_sha],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    with tarfile.open(archive_path, "r:") as archive:
        archive.extractall(destination, filter="data")


def main() -> int:
    workspace = Path(os.environ["GITHUB_WORKSPACE"])
    base_sha = os.environ.get("INPUT_BASE_SHA", "").strip()
    with tempfile.TemporaryDirectory(prefix="monetiza3d-osv-") as temp:
        temp_path = Path(temp)
        binary = temp_path / "osv-scanner"
        download_scanner(binary)

        current_status, current_report = scan(binary, workspace, temp_path / "current.json")
        current = findings(current_report, workspace)
        if current_status not in {0, 1} or (current_status == 1 and not current):
            raise RuntimeError("OSV-Scanner did not complete the head scan")
        baseline: dict[tuple[str, str, str, str, str], float | None] = {}
        if base_sha:
            base_directory = temp_path / "base"
            base_directory.mkdir()
            archive_base(base_sha, base_directory)
            base_status, base_report = scan(binary, base_directory, temp_path / "base.json")
            baseline = findings(base_report, base_directory)
            if base_status not in {0, 1} or (base_status == 1 and not baseline):
                raise RuntimeError("OSV-Scanner did not complete the base scan")

        new = {key: score for key, score in current.items() if key not in baseline}
        blocked = sum(level(score) in {"high", "critical"} for score in new.values())
        unknown = sum(level(score) == "unknown" for score in new.values())
        lower = len(new) - blocked - unknown
        print(
            "OSV-Scanner: "
            f"{blocked} new High/Critical, {lower} new lower-severity, "
            f"{unknown} new unknown-severity finding(s)."
        )
        if blocked:
            print("::error::New High/Critical dependency vulnerabilities block this change. Scanner output is withheld from logs.")
            return 1
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        # Do not print subprocess output or exception text that could contain repository data.
        print(f"::error::OSV-Scanner gate failed ({type(error).__name__}); raw output is withheld.")
        raise SystemExit(2)
