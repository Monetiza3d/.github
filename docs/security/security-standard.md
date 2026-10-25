# Padrão de segurança de código e supply chain

## CI obrigatório

Os repositórios de produto devem chamar o workflow reutilizável em `templates/.github/workflows/security.yml` após revisão e fixação do SHA deste repositório. O job recebe apenas código do checkout e `GITHUB_TOKEN` com `contents: read`; não usa `pull_request_target`, secrets de produção ou credenciais em PRs/forks.

Ferramentas padrão:

- OpenGrep para SAST, com regras de severidade Error como bloqueio e findings novos High/Critical como gate.
- TruffleHog para segredos confirmados e histórico Git. Em logs, mostrar apenas contagem e instrução de remediação; nunca imprimir resultado bruto/JSON, valor, token ou linha que contenha segredo.
- OSV-Scanner para dependências e lockfiles; bloquear vulnerabilidades novas High/Critical conforme política do serviço.
- zizmor e actionlint para workflows GitHub Actions.
- Trivy para imagens, Dockerfiles, IaC e dependências de sistema quando existirem.

O scan inicial cria um baseline por repositório. Achados existentes são registrados sem valor secreto, com arquivo/regra, severidade, responsável, mitigação e validade. Bloqueios por baseline não autorizam novos achados. Exceções têm prazo e responsável; falso positivo precisa de regra/linha justificada e escopo mínimo.

## Hardening da pipeline

- `permissions` é definido por workflow/job e começa como `contents: read`; elevar permissão apenas quando uma etapa requer e apenas naquela etapa.
- Ações externas usam SHA completo revisado, acompanhado do tag legível em comentário. Dependabot mantém os pins atualizados.
- O checkout de PR usa `pull_request`; nunca executar conteúdo não confiável com secrets por `pull_request_target`.
- Não publicar SARIF/artefatos de scanner que contenham código ou dados sensíveis sem avaliar acesso e redaction. Não usar upload que dependa de GitHub Advanced Security em repositórios privados sem confirmar entitlement.
- Imagens externas são fixadas por versão/digest e verificadas; builds não recebem credenciais em `ARG`, layers ou logs.

## Gestão de vulnerabilidades

Usar o processo de [SECURITY.md](../../SECURITY.md) e o [modelo de relato privado](../../templates/SECURITY_REPORT_TEMPLATE.md). Habilitar Private Vulnerability Reporting em cada repositório público quando disponível. O relato deve permanecer privado; manter titular e suplente de triagem, registrar evidências sem segredos e rotacionar credenciais expostas imediatamente.
