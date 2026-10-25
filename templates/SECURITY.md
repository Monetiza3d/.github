# Security policy

## Reporting a vulnerability

Do not report suspected vulnerabilities in public issues, discussions, or pull requests.

For a public repository with Private Vulnerability Reporting enabled, open that repository's **Security** tab and choose **Report a vulnerability**. Each public product repository must enable this feature individually. For a repository where the private reporting control is unavailable, contact the repository owner through a private channel before sharing technical details; the organization must configure a durable security contact before accepting external contributions or publishing additional repositories.

Include the affected repository and commit, affected versions, vulnerability category, impact, prerequisites, steps to reproduce, and any safe proof of concept. Do not include customer data or live credentials in the report. Maintainers should acknowledge reports within five business days, coordinate a fix and disclosure date with the reporter, and preserve relevant evidence.

## Maintainer response

The security owner and a backup maintainer are assigned per repository. A confirmed exposed credential is revoked or disabled first, then rotated, and checked for reuse. Preserve logs and relevant commit/build identifiers. Record scope, impact, containment, remediation, and disclosure decisions in a private incident record. Do not place secret values in issues, logs, CI artifacts, or incident notes.

## Supported versions

Security fixes are applied to the default branch and the latest released version of each service. Older releases are supported only when a repository explicitly documents an exception with an owner and expiry date.
