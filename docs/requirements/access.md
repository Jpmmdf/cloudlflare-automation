# Acessos e Tokens

Este documento descreve como obter e configurar corretamente os acessos e tokens necessários para operar a automação dos serviços DNS com Cloudflare utilizando Terraform e Terragrunt na RNP.

## Acesso ao Cloudflare

### Gerando Tokens de API

Os tokens do Cloudflare são utilizados para que Terraform e Terragrunt realizem chamadas automáticas e seguras à API do Cloudflare. Para gerar um token:

1. Faça login na sua conta do Cloudflare.
2. Navegue até **Meu perfil > Tokens de API**.
3. Clique em **Criar Token** e selecione o template "Editar DNS".
4. Configure as permissões conforme abaixo:

| Permissão            | Escopo                      |
|----------------------|-----------------------------|
| Zone.DNS             | Todas as zonas necessárias  |
| Zone.Read            | Todas as zonas necessárias  |
| Zone.Settings.Read   | Todas as zonas necessárias  |

3. Salve o token gerado em local seguro, pois não será exibido novamente.

### Segurança dos Tokens

- Nunca compartilhe tokens publicamente ou com usuários não autorizados.
- Armazene os tokens utilizando ferramentas seguras como o GitLab Secrets ou Vault.

## Acesso ao GitLab da RNP

Para operar corretamente, é necessário possuir acesso ao GitLab institucional da RNP.

### Permissões no GitLab

- Usuários que realizam merge requests ou atualizações no código devem ter permissões de **Developer**.
- Usuários responsáveis pela revisão e aprovação devem possuir permissões de **Maintainer** ou superiores.

## Configuração dos Tokens e Variáveis no GitLab CI/CD

1. No projeto GitLab, vá até **Settings > CI/CD**.
2. Na seção **Variables**, adicione as seguintes variáveis:

| Nome da Variável             | Descrição                                | Tipo      | Exemplo |
|------------------------------|-------------------------------------------|------------|---------|
| `TF_VAR_cloudflare_api_token`| Token de API do Cloudflare                | Protegido | `xxxx` |
| `TF_VAR_cloudflare_zone_id`  | ID da Zona DNS no Cloudflare              | Protegido | `xxxx` |
| `TF_VAR_STATE_BUCKET`        | Nome do Bucket S3 usado como backend Terraform | Protegido | `terraform-state-rnp` |

- Configure essas variáveis como **Protegidas** e **Mascaradas** para garantir segurança adicional.

## Acesso Opcional ao Backstage

Caso o Backstage esteja em uso, certifique-se de que:

- Usuários tenham acesso básico à plataforma.
- Esteja configurada a integração adequada com o GitLab, permitindo a abertura e o acompanhamento de solicitações.

## Gerenciamento Seguro de Secrets

Para aumentar a segurança, é recomendado utilizar soluções como Hashicorp Vault ou GitLab Secrets para armazenar e gerenciar as credenciais e chaves sensíveis.

---

Essas configurações garantirão uma operação segura, automatizada e eficiente no gerenciamento de DNS na RNP.