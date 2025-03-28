# Pré-requisitos

Este documento apresenta os pré-requisitos necessários para implementar e operar corretamente a automação do gerenciamento DNS no Cloudflare com Terraform e Terragrunt na RNP.

## Pré-requisitos Gerais

Antes de iniciar, certifique-se de que os seguintes itens estejam disponíveis e configurados adequadamente:

### Acesso ao Cloudflare

- **Conta Cloudflare ativa**: Acesso administrativo ou com permissões adequadas.
- **Chaves API**: Tokens com permissões suficientes para criar, editar e remover registros DNS no Cloudflare.

### Acesso ao GitLab Institucional da RNP

- Acesso ao Git institucional da RNP disponível em [git.rnp.br](https://git.rnp.br/).
- Permissões necessárias no repositório do projeto:
  - Usuários operadores: **Developer**
  - Revisores/Aprovadores: **Maintainer** ou superior

### Ferramentas Obrigatórias

- **Terraform**:
  - Versão recomendada: `>= 1.6.x`
  - [Download do Terraform](https://developer.hashicorp.com/terraform/downloads)

- **Terragrunt**:
  - Versão recomendada: `>= 0.54.x`
  - [Instalação Terragrunt](https://terragrunt.gruntwork.io/docs/getting-started/install/)

- **Git CLI**:
  - Versão recomendada: última versão estável
  - [Instalação Git](https://git-scm.com/downloads)

### Backend Terraform

- Bucket S3 já criado e configurado para armazenar remotamente o estado do Terraform.
- Variável `TF_VAR_STATE_BUCKET` configurada com o nome do bucket.

### Ferramentas Opcionais (recomendadas)

- **Python**:
  - Versão recomendada: `>= 3.10.x`
  - Necessário para scripts auxiliares e automações adicionais
  - [Instalação Python](https://www.python.org/downloads/)

- **MkDocs (para documentação)**:
  ```bash
  pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin
  ```

### Rede e Segurança

- Acesso à internet para comunicação com as APIs públicas do Cloudflare via HTTPS (`https://api.cloudflare.com`).
- Garantir permissões mínimas para acesso à API e aos recursos:
  - Zone.DNS
  - Zone.Read
  - Zone.Settings.Read

- As variáveis sensíveis como chaves API devem ser armazenadas com segurança no GitLab CI/CD.

---

Seguir estes pré-requisitos garante uma operação eficaz e segura da automação de DNS na RNP.

