# Monetiza3D

Monetiza3D is a SaaS platform for businesses that operate additive-manufacturing and 3D-printing workflows.

The organization maintains independent repositories for each product surface and bounded business service. Its public organization defaults and engineering standards are maintained in [`.github`](https://github.com/Monetiza3d/.github).

## Development principles

- Separate repositories and independently deployable services; no product monorepo.
- TypeScript for web and cloud services; the local printer edge agent is a separately scoped future component.
- Containers from the first implementation, with Kubernetes as the planned cloud orchestration target.
- Use the latest stable, supported dependencies and official reference documentation, verified at adoption and continuously reviewed.
- Report vulnerabilities privately; do not disclose suspected vulnerabilities in public issues.
