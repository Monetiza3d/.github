# Onboarding de repositórios

## Repositório novo

1. Escolher nome pelo domínio/superfície no [catálogo de serviços](architecture/service-catalog.md). Uma unidade implantável por repositório; nunca juntar serviços em monorepo.
2. Manter repositório de produto privado por padrão até decisão de publicação. Usar `.github` público como fonte de community health files onde GitHub aplicar defaults.
3. Copiar para o repositório privado os arquivos de `templates/`, ajustando nome, equipe responsável e contratos. Os defaults do GitHub não sincronizam workflows, dependabot, licenças ou políticas para repositórios existentes.
4. Criar Dockerfile com usuário não-root, build multi-stage, pin de imagem base, health/readiness endpoint, encerramento gracioso e sem segredo embutido.
5. Configurar `GITHUB_TOKEN` read-only, Dependabot, workflow reutilizável de segurança fixado por SHA, CODEOWNERS quando houver equipe definida, branch rules/required checks e acesso mínimo.
6. Criar `.ai-memory.toml` com workspace `Monetiza3d`, projeto igual ao nome canônico do repositório e estratégia `repo-root`.
7. Registrar owner primário e suplente, domínio, dados/banco próprios, OpenAPI, dependências de outros serviços e fase do roadmap.
8. Antes de publicar código: confirmar licença/titular, canal privado de segurança, secrets scanning, branch policy e política de dependências atualizadas.

## Verificação de conformidade

O owner confirma em PR inicial: template de issue/PR, workflow de segurança, dependabot, licença aprovada, container scan condicional, pins de ações e imagens, documentação oficial com data, runbook de migração/backup e classificação de dados. Repositórios sem esse registro não são considerados prontos para produção.
