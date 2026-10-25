# Padrão de containers e Kubernetes

## Container desde o primeiro serviço

- Cada aplicação/serviço tem imagem própria, build reproduzível e publicação independente em registry da organização.
- Imagens usam usuário não-root, estágio de build separado, dependências de runtime mínimas, `.dockerignore`, tags imutáveis e digest promovido entre ambientes.
- Configuração vem do ambiente/secret store, nunca de valores embutidos na imagem. Nenhuma credencial é passada por `ARG`, camada ou log.
- Serviços expõem health/readiness checks, encerram de forma graciosa, aplicam timeout e limites de recursos, e escrevem logs estruturados em stdout/stderr.
- Docker Compose é o caminho local para integrar o serviço com dependências. Dados persistentes usam volumes nomeados; dados de desenvolvimento não são commitados.
- Verificar imagens e dependências com Trivy; publicar SBOM quando houver imagem de aplicação; fixar imagens base por versão e digest e atualizar por PR.

## Kubernetes como destino de nuvem

Os contratos de execução devem ser compatíveis com Kubernetes desde o início, mas manifests e operação de cluster são introduzidos quando houver ambiente e necessidade operacional.

- Deployments stateless para BFF e serviços HTTP; Jobs/CronJobs para tarefas finitas e agendadas.
- ConfigMaps para configuração não sensível e Secrets integrados a um gerenciador de segredos; proibir segredo literal em manifests e GitOps.
- Probes de startup, readiness e liveness devem refletir o estado real da aplicação. Readiness não deve depender de serviços opcionais.
- Aplicar requests/limits, política de reinício, graceful shutdown, probes, NetworkPolicies e identidade de workload com privilégio mínimo.
- Gerenciar PostgreSQL com armazenamento persistente, backups externos, restauração ensaiada, atualização compatível e plano de recuperação. O banco não fica dentro do container da aplicação. A escolha entre operador PostgreSQL no cluster e serviço externo fica para a decisão de plataforma.
- Edge Agent roda como container no ambiente local do cliente e não é presumido como workload do cluster de nuvem; documentar permissões explícitas de USB e rede.

## Fluxo de entrega

Construir uma imagem uma vez, identificá-la por digest e promovê-la entre ambientes. Deploys são independentes por serviço; rollback aponta para o digest anterior. Kubernetes será ativado após definir operação, backup, observabilidade e ownership de cluster.
