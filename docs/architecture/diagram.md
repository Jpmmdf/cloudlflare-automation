# Diagramas da Arquitetura

Este documento apresenta diagramas que ilustram a arquitetura e os fluxos operacionais da automação de DNS utilizando Cloudflare, Terraform, Terragrunt e GitLab na RNP.

## Diagrama Geral da Arquitetura

```mermaid
graph LR
  Usuario[Usuário/Área Técnica] -->|Solicitação via GitLab ou Backstage| GitLab
  subgraph GitLab
    MR[Merge Request] --> CI[Pipeline CI/CD]
  end
  CI -->|Executa| Terraform
  Terraform --> Terragrunt
  Terragrunt --> Cloudflare
  Cloudflare --> DNS[Registros DNS Atualizados]
```

## Fluxo Detalhado do Pipeline CI/CD

```mermaid
graph TD
  A[Merge Request aberto no GitLab] --> B[Validação de sintaxe e segurança]
  B --> C[Testes automatizados de Terraform]
  C --> D[Aprovação Manual Opcional]
  D --> E[Aplicação Terraform/Terragrunt]
  E --> F[Provisionamento em Cloudflare]
  F --> G[Confirmação e Logs]
```

## Diagrama de Componentes

```mermaid
flowchart TB
  subgraph Usuários
    U1[Usuário Técnico]
    U2[Usuário não Técnico via Backstage]
  end

  subgraph Ferramentas
    TF[Terraform]
    TG[Terragrunt]
    GL[GitLab]
    CF[Cloudflare]
    BS[Backstage]
  end

  U1 --> GL
  U2 --> BS
  BS --> GL
  GL --> TF
  TF --> TG
  TG --> CF
```

## Considerações adicionais

- Os diagramas acima podem ser ajustados conforme mudanças ou melhorias na arquitetura.

