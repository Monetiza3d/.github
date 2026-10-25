#!/usr/bin/env python3
"""Ensure private-repository starter copies match organization defaults."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    (".github/ISSUE_TEMPLATE/config.yml", "templates/.github/ISSUE_TEMPLATE/config.yml"),
    (".github/ISSUE_TEMPLATE/bug_report.yml", "templates/.github/ISSUE_TEMPLATE/bug_report.yml"),
    (".github/ISSUE_TEMPLATE/feature_request.yml", "templates/.github/ISSUE_TEMPLATE/feature_request.yml"),
    (".github/ISSUE_TEMPLATE/documentation.yml", "templates/.github/ISSUE_TEMPLATE/documentation.yml"),
    (".github/PULL_REQUEST_TEMPLATE.md", "templates/.github/PULL_REQUEST_TEMPLATE.md"),
    ("SECURITY.md", "templates/SECURITY.md"),
    ("CONTRIBUTING.md", "templates/CONTRIBUTING.md"),
    ("SUPPORT.md", "templates/SUPPORT.md"),
    ("CODE_OF_CONDUCT.md", "templates/CODE_OF_CONDUCT.md"),
)


def main() -> int:
    drift = [
        f"{source} != {copy}"
        for source, copy in PAIRS
        if (ROOT / source).read_bytes() != (ROOT / copy).read_bytes()
    ]
    if drift:
        print("Organization defaults and repository template copies have drift:")
        for item in drift:
            print(f"- {item}")
        return 1
    print(f"Template sync: {len(PAIRS)} pairs match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
