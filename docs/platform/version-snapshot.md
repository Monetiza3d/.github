# Snapshot de versões verificadas

Verificação feita em **2026-10-25**. Estes valores registram o estado oficial naquele dia; não são pins permanentes.

| Projeto | Versão estável mais recente verificada | Fonte |
|---|---:|---|
| OpenAPI Specification | 3.2.1 | https://spec.openapis.org/oas/v3.2.1.html |
| PostgreSQL | 18.6 | https://www.postgresql.org/support/versioning/ |
| Node.js LTS | 24.22.1 | https://nodejs.org/en/about/previous-releases |
| OpenGrep | 1.32.0 | https://github.com/opengrep/opengrep/releases/tag/v1.32.0 |
| TruffleHog | 3.99.7 | https://github.com/trufflesecurity/trufflehog/releases/tag/v3.99.7 |
| OSV-Scanner | 2.7.0 | https://github.com/google/osv-scanner/releases/tag/v2.7.0 |
| Trivy | 0.76.1 | https://github.com/aquasecurity/trivy/releases/tag/v0.76.1 |
| zizmor CLI | 1.31.1 | https://github.com/zizmorcore/zizmor/releases/tag/v1.31.1 |
| actionlint | 1.7.12 | https://github.com/rhysd/actionlint/releases/tag/v1.7.12 |

PostgreSQL 19 não foi escolhido porque estava em release candidate na data da verificação. OpenAPI usa o patch estável mais recente da linha atual. Para Node.js, o padrão de produção seleciona o LTS mais recente, não o canal Current.
