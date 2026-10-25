# Atualidade de dependências e documentação de referência

## Requisito

Na fundação e em toda adoção ou atualização, usar a versão estável mais recente publicada pelo mantenedor oficial para dependências, runtimes, padrões, ferramentas, imagens-base e documentação de referência. “Mais recente” significa GA estável e suportada; beta, alpha, nightly, preview e release candidate não entram em produção. Para runtimes com canal LTS, preferir a linha LTS mais recente em produção e manter seu patch atualizado.

Verificar a versão nas fontes oficiais no momento do trabalho; não reutilizar pins copiados de um ADR antigo ou de outro projeto sem nova verificação. Fixar versões exatas em lockfiles, containers por versão/digest e GitHub Actions por SHA completo. Toda divergência temporária exige ADR/issue com justificativa, responsável e data de revisão/expiração.

## Documentação

- Usar documentação oficial atual do mantenedor ou da organização responsável pelo padrão.
- Em ADRs, registrar versão consultada, URL direta da referência, data da verificação e compatibilidade observada.
- Ao atualizar uma dependência, atualizar também as referências e exemplos que ficaram desatualizados; remover links para versões EOL.
- Diferenciar versões estáveis de versões preview quando a fonte oficial publicar ambas.

## Automação e cadência

- Habilitar Dependabot para GitHub Actions, npm e Docker nos repositórios aplicáveis, com propostas semanais e lockfiles atualizados.
- Revisar atualizações e avisos de segurança em cada PR; não deixar alertas High/Critical sem triagem, responsável e prazo.
- Revalidar versões de padrões e ferramentas de release nos trabalhos de fundação, mensalmente e antes de uma nova fase de produto.
- As referências correntes verificadas para esta fundação estão em [`version-snapshot.md`](version-snapshot.md). Esse snapshot é uma medição datada, não uma autorização para manter a mesma versão indefinidamente.

## Snapshot verificado em 2026-10-25

| Componente | Versão corrente selecionada | Referência oficial |
|---|---:|---|
| OpenAPI Specification | 3.2.1 | https://spec.openapis.org/oas/v3.2.1.html |
| PostgreSQL | 18.6 estável; PostgreSQL 19 ainda RC em 25/10/2026 | https://www.postgresql.org/support/versioning/ |
| Node.js para produção | 24.22.1 LTS | https://nodejs.org/en/about/previous-releases |

Os demais pins operacionais da pipeline estão no manifesto [`tool-versions.json`](../../tool-versions.json) e devem ser renovados pelas propostas de dependência e pela revisão de atualidade.
