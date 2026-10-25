#!/usr/bin/env python3
"""Fail with a safe summary when pinned GitHub releases fall behind upstream."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tool-versions.json"


def latest_release(repository: str) -> str:
    request = urllib.request.Request(
        f"https://github.com/{repository}/releases/latest",
        headers={"User-Agent": "Monetiza3d-version-freshness"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        final_url = response.geturl()
    marker = "/releases/tag/"
    if marker not in final_url:
        raise ValueError(f"Could not resolve latest release for {repository}")
    return final_url.split(marker, 1)[1].split("/", 1)[0]


def tag_commit(repository: str, tag: str) -> str:
    result = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{repository}.git", f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    refs = [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
    if not refs:
        raise ValueError(f"Could not resolve release tag for {repository}")
    return refs[-1]


def ghcr_manifest_digest(image: str) -> str:
    registry_path, tag = image.removeprefix("ghcr.io/").split(":", 1)
    token_request = urllib.request.Request(
        f"https://ghcr.io/token?scope=repository:{registry_path}:pull",
        headers={"User-Agent": "Monetiza3d-version-freshness"},
    )
    with urllib.request.urlopen(token_request, timeout=20) as response:
        token = json.load(response)["token"]
    request = urllib.request.Request(
        f"https://ghcr.io/v2/{registry_path}/manifests/{tag}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": ", ".join(
                [
                    "application/vnd.oci.image.index.v1+json",
                    "application/vnd.docker.distribution.manifest.list.v2+json",
                    "application/vnd.oci.image.manifest.v1+json",
                    "application/vnd.docker.distribution.manifest.v2+json",
                ]
            ),
            "User-Agent": "Monetiza3d-version-freshness",
        },
        method="HEAD",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.headers["Docker-Content-Digest"]


def normalize(version: str) -> str:
    return version.removeprefix("v")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    stale: list[str] = []
    errors: list[str] = []
    workflow = (ROOT / ".github/workflows/security-reusable.yml").read_text()
    caller_template = (ROOT / "templates/.github/workflows/security.yml").read_text()
    osv_action = (ROOT / "actions/osv-delta/run.py").read_text()
    for name, item in manifest["tools"].items():
        repository = item.get("release_repository")
        if not repository:
            continue
        try:
            latest = latest_release(repository)
            if item.get("sha") and tag_commit(repository, item["version"]) != item["sha"]:
                stale.append(f"{name}: pinned SHA does not match release tag {item['version']}")
        except urllib.error.HTTPError as error:
            errors.append(f"{name} (HTTP {error.code})")
            continue
        except (KeyError, OSError, ValueError, subprocess.SubprocessError, urllib.error.URLError, json.JSONDecodeError):
            errors.append(name)
            continue
        if normalize(item["version"]) != normalize(latest):
            stale.append(f"{name}: pinned {item['version']}, upstream {latest}")

    inline_pins = {
        "opengrep": f'opengrep-version: "{manifest["tools"]["opengrep"]["version"]}"',
        "trufflehog": f'ghcr.io/trufflesecurity/trufflehog@{manifest["tools"]["trufflehog"]["container_digest"]}',
        "actions_checkout": f'actions/checkout@{manifest["tools"]["actions_checkout"]["sha"]}',
        "osv_delta_action": f'Monetiza3d/.github/actions/osv-delta@{manifest["tools"]["osv_delta_action"]["commit"]}',
        "opengrep_action": f'platform-sec/opengrep-action@{manifest["tools"]["opengrep_action"]["sha"]}',
        "trivy_action": f'aquasecurity/trivy-action@{manifest["tools"]["trivy_action"]["sha"]}',
        "trivy": f'version: "{manifest["tools"]["trivy"]["version"]}"',
        "zizmor_action": f'zizmorcore/zizmor-action@{manifest["tools"]["zizmor_action"]["sha"]}',
        "zizmor": f'version: "{manifest["tools"]["zizmor"]["version"]}"',
        "actionlint": f'actionlint/releases/download/v{manifest["tools"]["actionlint"]["version"]}',
    }
    for name, reference in inline_pins.items():
        if reference not in workflow:
            stale.append(f"{name}: workflow pin differs from tool-versions.json")
    if (
        f'VERSION = "{manifest["tools"]["osv_scanner"]["version"]}"' not in osv_action
        or f'SHA256 = "{manifest["tools"]["osv_scanner"]["sha256"]}"' not in osv_action
    ):
        stale.append("osv_scanner: action version/checksum differs from tool-versions.json")
    core_workflow_ref = f'Monetiza3d/.github/.github/workflows/security-reusable.yml@{manifest["tools"]["core_workflow"]["commit"]}'
    if core_workflow_ref not in caller_template:
        stale.append("private repository caller template pin differs from tool-versions.json")
    try:
        trufflehog = manifest["tools"]["trufflehog"]
        current_digest = ghcr_manifest_digest(trufflehog["container_image"])
        if current_digest != trufflehog["container_digest"]:
            stale.append(
                f"trufflehog: image digest for {trufflehog['container_image']} changed upstream"
            )
    except urllib.error.HTTPError as error:
        errors.append(f"trufflehog container image digest (HTTP {error.code})")
    except (KeyError, OSError, ValueError, subprocess.SubprocessError, urllib.error.URLError, json.JSONDecodeError):
        errors.append("trufflehog container image digest")

    if errors:
        print("Could not verify upstream releases for: " + ", ".join(errors), file=sys.stderr)
    if stale:
        print("Version pins need review:")
        for item in stale:
            print(f"- {item}")
    if errors or stale:
        return 1
    print("All GitHub-release pins match their latest stable releases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
