# Gerenciamento de DNS

Este documento detalha o processo para criar, modificar ou remover registros DNS utilizando a automação do Cloudflare com Terraform e Terragrunt na RNP.

## Visão Geral

O gerenciamento dos registros DNS é realizado através da edição de arquivos Terraform/Terragrunt e da execução automática dos pipelines do GitLab.

## Estrutura para Gerenciamento DNS

Os registros DNS são definidos em arquivos `terragrunt.hcl`, que utilizam módulos Terraform compartilhados.

Exemplo da estrutura para registros DNS:

```plaintext
terraform/
├── rnp_account/
│   └── demo.br/
│       └── dns/
│           ├── root/
│           │   └── terragrunt.hcl
│           └── www/
│               └── terragrunt.hcl
```

## Criando ou Alterando Registros DNS

### Passo 1: Acesse o diretório correto

Vá até o diretório específico que representa a zona/subdomínio desejado. Por exemplo:

```bash
cd terraform/rnp_account/demo.br/dns/www/
```

### Estrutura do `terragrunt.hcl`

```hcl
terraform {
  source = "${get_repo_root()}/terraform/shared/core/dns"
}

include "root" {
  path = find_in_parent_folders("root.hcl")
}

inputs = {
  dns_records = [
    {
      name        = "root"
      type        = "A"
      value       = "192.168.1.1"
      ttl         = 1
      proxied     = false
      comment     = "None"
      settings    = {}
      owner       = "auto-import"
      environment = "production"
    }
  ]
}
```

- **`name`**: Nome do registro DNS (ex: "root").
- **`type`**: Tipo do registro (A, CNAME, MX, etc.).
- **`value`**: Valor do registro DNS (IP, domínio, etc.).
- **`ttl`**: Tempo de vida em segundos (`1` para automático).
- **`proxied`**: `true` para ativar proxy Cloudflare, `false` para desativar.
- **`comment`**: Comentário opcional sobre o registro.
- **`settings`**: Configurações adicionais.
- **`owner`**: Indica a origem do registro.
- **`environment`**: Define o ambiente relacionado ao registro.

## Fluxo para Realizar Alterações

### Criar uma Branch

Crie uma nova branch para a alteração:

```bash
git checkout -b nome-da-branch
```

### Editar Registros DNS

Adicione ou altere os registros necessários no arquivo `terragrunt.hcl`.

### Commit e Merge Request

Utilize o padrão Conventional Commits para o commit:

```bash
git add .
git commit -m "feat: adiciona registro DNS root para demo.br"
git push origin nome-da-branch
```

Abra um Merge Request no GitLab para revisão e aprovação.

## Removendo Registros DNS

Para remover um registro DNS, remova a entrada correspondente da lista no arquivo `terragrunt.hcl`:

```hcl
inputs = {
  dns_records = [
    # Remova o registro desejado desta lista.
  ]
}
```

Faça o commit e abra o Merge Request:

```bash
git commit -m "feat: remove registro DNS root para demo.br"
```

## Pipeline Automático

Após aprovação e merge, o pipeline GitLab executará automaticamente:

- Validação das alterações com Terraform/Terragrunt.
- Aplicação automática das mudanças diretamente no Cloudflare.

**Observação:** Não execute Terragrunt diretamente localmente; todas as validações são feitas exclusivamente através do pipeline GitLab.

---

Seguindo essas orientações, é possível gerenciar eficientemente registros DNS utilizando a automação na RNP.