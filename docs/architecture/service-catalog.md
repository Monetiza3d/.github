# Catálogo inicial de domínios e serviços

Este catálogo deriva a ordem de fases dos documentos de brainstorm do Monetiza3D e atualiza a topologia para serviços implantáveis em repositórios independentes. As fases definem sequência de implementação, não uma obrigação de lançar todos os serviços ao mesmo tempo.

| Fase | Repositório/serviço previsto | Responsabilidade inicial |
|---|---|---|
| 1 | `identity-service` | Identidades, login/OIDC, MFA, sessões, memberships, empresas/unidades, papéis e governança de privacidade. Cada serviço de domínio continua responsável por autorizar ações sobre seus próprios recursos. |
| 2 | `inventory-service` | Insumos, materiais, carretéis, acessórios, peças prontas, movimentos, disponibilidade e reservas de estoque. |
| 3 | `cost-engine-service` | Perfis de máquina e operação, cálculo de custos, precificação, presets e orçamentos. |
| 4 | `order-management-service` | Clientes, encomendas, ciclo de venda/produção, CRM operacional, alocação e estorno idempotente. |
| 5 | `printer-fleet-service` + `edge-agent` | Pareamento e gestão de frota, protocolos de telemetria e agente junto ao hardware. O agente pode precisar de acesso local a USB/rede. |
| 6 | `affiliate-broker-service` | Recomendações de reposição, fornecedores, integrações B2B e redes de afiliados. |
| 7 | `global-admin-analytics-service` | Administração da plataforma e analytics agregados com proteção de privacidade. |

Componentes de superfície e plataforma, também em repositórios separados:

- `portal`: aplicação autenticada React.
- `brand-site`: site público da marca, independente do portal.
- `bff`: API de experiência do portal, sem ser dono dos dados de domínio.
- `platform-infra`: infraestrutura, deploy, observabilidade e futura configuração Kubernetes.

## Limites de serviço

- Cada serviço possui repositório, pipeline, versão, deploy, contratos, migrações e ownership próprios. Não existe monorepo de produto.
- O `identity-service` publica identidade e memberships; serviços de domínio validam identidade e aplicam autorização local. Nenhum serviço lê tabelas internas de outro.
- Cada serviço é proprietário de seu banco/schema e usa credencial de banco própria. Um cluster PostgreSQL pode ser compartilhado no começo, mas não se compartilham tabelas nem se fazem joins entre domínios.
- OpenAPI versionado descreve APIs HTTP. Mudanças incompatíveis exigem nova versão ou janela explícita de migração. Eventos duráveis são introduzidos quando um fluxo assíncrono exigir entrega confiável; não criar broker por antecipação.
- Tenant inicial: empresa → unidade/site. Isolamento é aplicado em consultas e autorização; RLS pode atuar como defesa adicional com contexto por transação.

## Ordem de entrega prevista

Fase 1 é a fundação de identidade e tenancy. As Fases 2 e 3 trazem o primeiro valor funcional: estoque e cálculo de custos/orçamentos. A Fase 4 adiciona encomendas, vendas e CRM, apoiados por estoque e orçamento. Fases 5–7 são roadmap futuro.

Os documentos originais propõem Vue e monólito modular; essas decisões foram substituídas pela direção aprovada: React, repositórios separados e serviços independentes. Valkey não é dependência do MVP. O PostgreSQL pode compartilhar infraestrutura física no começo, mantendo propriedade lógica e credenciais segregadas.
