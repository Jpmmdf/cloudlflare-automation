# Componentes da Arquitetura

Este documento detalha cada componente chave utilizado na arquitetura de automação e gestão de DNS no Cloudflare na RNP, destacando as funções e responsabilidades específicas de cada um.

## Cloudflare

Cloudflare é a plataforma escolhida para hospedagem dos serviços DNS, fornecendo funcionalidades críticas como:

- DNS autoritativo de alta disponibilidade.
- Proteção contra ataques DDoS.
- API RESTful para gerenciamento e automação.
- Segurança integrada com WAF, controle de acesso e políticas de proteção avançadas.

## Terraform

Terraform é uma ferramenta de infraestrutura como código (IaC) usada para gerenciar recursos no Cloudflare com eficiência e segurança. Suas principais funções incluem:

- Provisão automática e consistente de recursos.
- Controle rigoroso sobre estados e versões da infraestrutura.
- Documentação automática da infraestrutura como código.
- Integração facilitada com CI/CD para automação completa.

## Terragrunt

Terragrunt é uma camada complementar ao Terraform, criada para facilitar a gestão de múltiplos ambientes e reduzir a complexidade operacional. Entre suas funções estão:

- Centralização e gerenciamento simplificado das configurações.
- Reutilização e modularização do código Terraform.
- Padronização na estrutura de pastas e arquivos.
- Execução simplificada de comandos Terraform através de wrappers automáticos.

## GitLab

O GitLab é a ferramenta de versionamento e integração contínua adotada pela RNP para desenvolvimento, revisão e automação. Suas responsabilidades incluem:

- Armazenamento seguro e controlado do código.
- Revisão de código (merge requests) com colaboração eficiente.
- Pipelines CI/CD para validação, testes automatizados e aplicação segura das mudanças na infraestrutura.
- Logs detalhados e rastreabilidade das alterações aplicadas.

## Backstage (opcional)

Backstage é uma plataforma aberta de desenvolvimento que oferece um portal de autoatendimento para equipes técnicas e não técnicas da RNP. Caso integrada, ela proporciona:

- Interface amigável para requisição e acompanhamento dos serviços DNS.
- Visão unificada dos recursos gerenciados via Terraform.
- Redução de barreiras técnicas ao permitir que usuários finais realizem tarefas técnicas através de uma interface simplificada.

## Ferramentas Adicionais

- **GitLab CI/CD**: Utilizado para automação completa do fluxo, desde testes até o provisionamento no Cloudflare.
- **Prometheus e Grafana** (opcional): Monitoramento e dashboards em tempo real, garantindo visibilidade operacional dos recursos e eventos da plataforma.
- **Vault** (opcional): Gerenciamento seguro das chaves de acesso e secrets utilizados pela infraestrutura.

Cada componente listado desempenha papel fundamental na garantia de uma operação segura, eficiente e escalável dentro da arquitetura proposta.

