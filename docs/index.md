# Automação de DNS com Terraform e Terragrunt

## Visão Geral
Este repositório contém a configuração para automação da gestão de DNS da xpto no Cloudflare utilizando **Terraform** e **Terragrunt**. Além disso, está integrado ao **Backstage** e **GitLab CI/CD** para permitir que as áreas de negócio criem e gerenciem registros DNS de forma automatizada.

## Tecnologias Utilizadas
- **Terraform**: Provisionamento de infraestrutura como código.
- **Terragrunt**: Gerenciamento e organização modular do Terraform.
- **Cloudflare**: Gerenciamento de DNS.
- **Backstage**: Interface para automação dos registros DNS.
- **GitLab CI/CD**: Automatização do fluxo de aplicação das mudanças.

## Estrutura do Repositório
Seguindo as **melhores práticas do Cloudflare**, utilizamos uma estrutura baseada em **contas, zonas e produtos**:

```plaintext
terraform/
├── terragrunt.hcl                        # Configuração global do Terragrunt
├── xpto_account                           # Conta principal
│   ├── users                             # Diretório para gestão de usuários (zoneless)
│   │   ├── provider.tf                   # Configuração do provider Cloudflare
│   │   ├── users.tf                      # Gestão de usuários
│   │   └── vars.tf                        # Variáveis
│   ├── xpto.br                            # Domínio principal
│   │   ├── dns                           # Diretório para registros DNS
│   │   │   ├── provider.tf                # Provider do Cloudflare
│   │   │   ├── vars.tf                    # Variáveis do DNS
│   │   │   ├── dns.tf                     # Registros DNS agrupados por produto
│   │   ├── page_rules                    # Diretório para regras de página
│   │   │   ├── provider.tf                # Provider do Cloudflare
│   │   │   ├── vars.tf                    # Variáveis de Page Rules
│   │   │   ├── page_rules.tf              # Configuração de regras de página
│   ├── outra_zona                         # Outro domínio gerenciado
│   │   ├── dns
│   │   │   ├── provider.tf
│   │   │   ├── vars.tf
│   │   │   ├── dns.tf
│   │   ├── page_rules
│   │   │   ├── provider.tf
│   │   │   ├── vars.tf
│   │   │   ├── page_rules.tf
```

## Como Utilizar
### 1️⃣ Configurar o Terraform
```sh
terraform init
terraform plan
terraform apply -auto-approve
```

### 2️⃣ Utilizar o Terragrunt
```sh
terragrunt run-all apply
```

### 3️⃣ Pipeline GitLab CI/CD
O pipeline do GitLab executa automaticamente a validação e aplicação dos registros.
Exemplo de `.gitlab-ci.yml`:

```yaml
stages:
  - validate
  - apply

validate:
  script:
    - terraform init
    - terraform validate
  only:
    - merge_requests

apply:
  script:
    - terraform apply -auto-approve
  only:
    - main
```

## Contribuindo
1. Faça um fork do repositório.
2. Crie uma branch com sua feature (`git checkout -b minha-feature`).
3. Faça commit das suas mudanças (`git commit -m 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin minha-feature`).
5. Abra um Pull Request.

## Contato
Dúvidas ou sugestões? Entre em contato com a equipe responsável.

---
Essa documentação está em constante evolução. Para mais detalhes, consulte a pasta `docs/`.

