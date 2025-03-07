# Automação de DNS com Terraform e Terragrunt

## Visão Geral

Este repositório contém a configuração para automação da gestão de DNS no Cloudflare utilizando **Terraform** e **Terragrunt**. Além disso, está integrado ao **Backstage** e **Github Actions** para permitir que as áreas de negócio criem e gerenciem registros DNS de forma automatizada.

## Tecnologias Utilizadas

- **Terraform**: Provisionamento de infraestrutura como código.
- **Terragrunt**: Gerenciamento e organização modular do Terraform.
- **Cloudflare**: Gerenciamento de DNS.
- **Backstage**: Interface para automação dos registros DNS.
- **MkDocs**: Ferramenta para documentação do projeto.

## Estrutura do Repositório

A estrutura foi reorganizada para utilizar **Terragrunt**, facilitando a gestão modular e reutilizável das zonas DNS e outros módulos do Cloudflare, como **Page Rules, WAF e Rate Limiting**.

```plaintext
terraform/
├── root.hcl                              # Configuração global do Terragrunt
├── xpto_account                           # Conta principal
│   ├── demo.br                           # Zona "demo.br"
│   │   ├── dns                           # Diretório para registros DNS
│   │   │   ├── root                      # Configuração para raiz da zona
│   │   │   │   ├── terragrunt.hcl        # Configuração do Terragrunt
│   │   │   ├── www                       # Configuração para subdomínio www
│   │   │   │   ├── terragrunt.hcl        # Configuração do Terragrunt
│   │   ├── page_rules                    # Configuração de regras de página
│   │   │   ├── terragrunt.hcl            # Configuração do Page Rules
│   │   ├── waf                           # Configuração do WAF
│   │   │   ├── terragrunt.hcl            # Configuração do WAF
│   │   ├── rate_limiting                 # Configuração do Rate Limiting
│   │   │   ├── terragrunt.hcl            # Configuração do Rate Limiting
│   ├── shared                            # Módulos compartilhados
│   │   ├── core
│   │   │   ├── dns                       # Configuração base do DNS
│   │   │   │   ├── dns.tf                # Definição dos registros DNS
│   │   │   │   ├── providers.tf          # Configuração do provider Cloudflare
│   │   │   │   ├── vars.tf               # Variáveis utilizadas
│   │   │   ├── page_rules                # Módulo compartilhado de Page Rules
│   │   │   ├── waf                       # Módulo compartilhado de WAF
│   │   │   ├── rate_limiting             # Módulo compartilhado de Rate Limiting
```

## Configuração do Backend no Terragrunt

A configuração do backend para armazenar o **estado remoto** está definida globalmente no `root.hcl`, utilizando **S3 e DynamoDB**:

```hcl
remote_state {
  backend = "s3"
  config = {
    bucket         = "SEU_BUCKET_TERRAFORM_STATE"
    key            = "terraform.tfstate"
    region         = "REGION"
    encrypt        = true
    dynamodb_table = "NOME_DA_TABELA_DYNAMODB"
  }
}
```

Cada ambiente herda essa configuração através do `include` nos arquivos `terragrunt.hcl`:

```hcl
include {
  path = find_in_parent_folders()
}
```

## Como Utilizar

### 1️⃣ Inicializar o Terraform

```sh
terragrunt run-all init
```

### 2️⃣ Aplicar as Mudanças com Terragrunt

```sh
terragrunt run-all apply
```

Se precisar aplicar apenas um ambiente específico:

```sh
cd terraform/xpto_account/demo.br/dns/root
terragrunt apply
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

Esta documentação está em constante evolução. Para mais detalhes, consulte a pasta `docs/`.

## Documentação
Este projeto utiliza **MkDocs** para organizar e manter a documentação. Para visualizar a documentação localmente, execute:

```sh
mkdocs serve
```

Para gerar os arquivos estáticos da documentação:

```sh
mkdocs build
```

Para mais detalhes, consulte o arquivo `mkdocs.yml`.