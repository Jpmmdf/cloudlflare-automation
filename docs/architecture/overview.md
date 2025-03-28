# Visão Geral da Arquitetura

Este documento fornece uma visão abrangente da arquitetura utilizada para a automação e gerenciamento de DNS no Cloudflare, utilizando Terraform e Terragrunt na RNP.

## Contexto Geral

A solução tem como objetivo principal automatizar e simplificar a gestão dos registros DNS no Cloudflare, permitindo maior eficiência operacional, redução de erros humanos e maior autonomia para as áreas internas da RNP.

## Componentes Principais

A arquitetura é composta pelos seguintes componentes essenciais:

- **Cloudflare**: Provedor de serviços DNS gerenciado, garantindo disponibilidade, segurança e desempenho.
- **Terraform**: Ferramenta utilizada para provisionamento e gestão de infraestrutura como código (IaC), responsável pela criação e manutenção de recursos no Cloudflare.
- **Terragrunt**: Camada adicional sobre o Terraform, utilizada para simplificar o gerenciamento de múltiplos ambientes, reutilização de código, variáveis e organização estrutural.
- **GitLab**: Repositório de código e integração contínua da RNP, responsável pelo versionamento, revisão de código e automação dos pipelines.
- **Backstage** (opcional): Plataforma de desenvolvedores que pode ser integrada à solução para oferecer uma interface amigável e autoatendimento às áreas internas da RNP.

## Fluxo Geral de Operação

1. **Requisição**: As áreas internas ou responsáveis técnicos solicitam a criação ou modificação de registros DNS através do Backstage ou diretamente via merge request no GitLab.

2. **Validação**: O código Terraform passa por revisão e validação automática através do pipeline do GitLab CI/CD para assegurar boas práticas e segurança.

3. **Provisionamento**: Após validação, o pipeline automatizado aplica as mudanças utilizando Terraform/Terragrunt diretamente no Cloudflare.

4. **Monitoramento e Manutenção**: A equipe de operação monitora continuamente as mudanças através de logs e dashboards, realizando intervenções conforme necessário.

## Estrutura Organizacional do Código

A estrutura segue as melhores práticas recomendadas pelo Cloudflare e pela comunidade Terraform:

```
terraform/
├── accounts/
│   └── account-id/
│       └── zones/
│           └── example.com/
│               ├── dns.tf
│               └── terraform.tfvars
├── modules/
│   └── cloudflare_dns/
│       └── main.tf
└── terragrunt.hcl
```

- **accounts**: Agrupa as zonas DNS por conta do Cloudflare.
- **zones**: Contém arquivos específicos para cada zona DNS gerenciada.
- **modules**: Centraliza módulos Terraform reutilizáveis, evitando repetição de código.

## Considerações Adicionais

- O acesso ao Cloudflare é feito via API, sendo necessárias chaves específicas com as permissões adequadas.
- É fundamental manter os ambientes controlados e monitorados através de auditoria constante das modificações realizadas.

