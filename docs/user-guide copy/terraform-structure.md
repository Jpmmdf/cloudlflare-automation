# Estrutura Terraform

Este documento detalha a estrutura organizacional adotada no projeto para a automação de DNS na RNP, utilizando Terraform e Terragrunt, garantindo clareza, simplicidade e padronização.

## Estrutura Geral do Repositório

A estrutura do repositório é dividida conforme a seguinte hierarquia:

```plaintext
terraform/
├── root.hcl                              # Configuração global do Terragrunt
├── rnp_account                           # Conta principal
│   ├── demo.br                           # Zona "demo.br"
│   │   ├── dns                           # Diretório para registros DNS
│   │   │   ├── root                      # Configuração para raiz da zona
│   │   │   │   ├── terragrunt.hcl        # Configuração do Terragrunt
│   │   │   ├── www                       # Configuração para subdomínio www
│   │   │   │   ├── terragrunt.hcl        # Configuração do Terragrunt
│   │   ├── page_rules                    # Configuração de regras de página
│   │   │   ├── terragrunt.hcl            # Configuração das Page Rules
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

## Descrição dos Diretórios e Arquivos

### Diretório `rnp_account`

Este diretório representa a conta principal Cloudflare utilizada pela RNP.

- Cada zona DNS tem seu próprio subdiretório (exemplo: `demo.br`).
- Dentro de cada zona DNS, são organizados recursos específicos (DNS, Page Rules, WAF, Rate Limiting).

### Diretório `dns`

Responsável por organizar registros DNS por domínio ou subdomínio.

- Exemplo:
  - `root`: Configuração para a raiz da zona.
  - `www`: Configuração específica para o subdomínio "www".

### Diretórios adicionais

- `page_rules`: Configuração específica das regras de página do Cloudflare.
- `waf`: Configuração específica para Web Application Firewall (WAF).
- `rate_limiting`: Configuração específica para regras de Rate Limiting.

### Diretório `shared`

Contém módulos reutilizáveis compartilhados para simplificar a gestão e evitar repetição.

- `core`: Contém módulos fundamentais reutilizáveis por múltiplas zonas.
  - `dns`: Definições básicas dos registros DNS.
  - `page_rules`: Definições compartilhadas das regras de página.
  - `waf`: Configurações compartilhadas do WAF.
  - `rate_limiting`: Configurações compartilhadas de Rate Limiting.

### Arquivo `root.hcl`

Arquivo de configuração global do Terragrunt, centralizando configurações comuns e definindo o backend remoto (S3).

## Boas Práticas

- Sempre utilize módulos compartilhados para evitar duplicação de código.
- Separe claramente configurações específicas de cada zona das configurações compartilhadas.
- Use arquivos `terragrunt.hcl` para gerenciar o backend e variáveis comuns.

Seguir essa estrutura clara e organizada permite uma operação eficiente, escalável e padronizada dos recursos DNS no Cloudflare usando Terraform e Terragrunt na RNP.