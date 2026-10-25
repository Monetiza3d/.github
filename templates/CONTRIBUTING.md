# Contributing

## Before opening a change

- Open an issue for a feature or substantial change and identify the affected service/domain.
- Keep changes within the owning repository. Cross-service changes must update or preserve the published API/event contract and identify deployment ordering.
- Do not add real secrets, customer data, or production exports to source, examples, fixtures, or logs.
- Use current official documentation and record significant technology/version decisions in an ADR or the relevant repository document.

## Pull requests

Pull requests must describe the problem, behavior change, affected repositories/contracts, security and data impact, migration/rollback considerations, and verification performed. Link the issue and call out any dependency or API version change.

The repository's required checks must pass before merge. Security exceptions require a written rationale, an accountable owner, compensating controls, and an expiry date. Do not suppress a finding without recording those details.

## Intellectual property

External contributions are not accepted until the organization has published its approved written contribution and rights-assignment terms. A pull request alone is not treated as a transfer of copyright. Do not copy code or assets from personal or third-party repositories without checking their licenses and obtaining the required permission.
