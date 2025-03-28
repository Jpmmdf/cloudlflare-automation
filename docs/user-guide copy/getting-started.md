# Guia Inicial

Este guia tem como objetivo orientar os usuários técnicos e operadores da RNP nos primeiros passos para utilizar e operar a solução de automação de DNS com Cloudflare, Terraform e Terragrunt.

## Pré-requisitos

Certifique-se de ter cumprido todos os pré-requisitos detalhados em [Pré-requisitos](../requirements/prerequisites.md) e [Acessos e Tokens](../requirements/access.md).

## Instalação das Ferramentas

### Terraform

Instale o Terraform com o seguinte comando:

```bash
wget https://releases.hashicorp.com/terraform/<versao>/terraform_<versao>_linux_amd64.zip
unzip terraform_<versao>_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

### Git CLI

Instale o Git seguindo [este guia](https://git-scm.com/downloads).

## Configuração Inicial

### Clonando o repositório

Clone o repositório institucional:

```bash
git clone https://git.rnp.br/GTI/cloudflare
cd cloudflare-automation
```

### Configurando credenciais Cloudflare

Configure variáveis de ambiente localmente para testes:

```bash
export TF_VAR_cloudflare_api_token="seu-token-api"
export TF_VAR_cloudflare_zone_id="id-da-sua-zona"
```

### Backend Terraform

Configure corretamente o backend no arquivo `terragrunt.hcl` para armazenar o estado remotamente no S3:

```hcl
remote_state {
  backend = "s3"
  config = {
    bucket = "nome-do-seu-bucket-s3"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
```

## Fluxo Inicial de Operação

### Realizando uma alteração

1. Crie uma nova branch para a alteração:

```bash
git checkout -b nome-da-branch
```

2. Edite os arquivos Terraform/Terragrunt conforme necessário (por exemplo: adicionando registros DNS em `dns.tf`).

3. Realize o commit utilizando o padrão de Conventional Commits:

```bash
git add .
git commit -m "feat: adiciona novo registro DNS para exemplo.com"
git push origin nome-da-branch
```

Exemplos de Conventional Commits:

- `feat`: nova funcionalidade
- `fix`: correção de um bug
- `docs`: mudanças na documentação
- `chore`: atualizações menores ou tarefas administrativas

2. Abra um Merge Request no GitLab e aguarde revisão e aprovação. A pipeline do GitLab executará automaticamente a validação com Terragrunt/Terraform.

### Validação no Pipeline

Não execute Terragrunt diretamente localmente, pois a validação das alterações será feita exclusivamente através do pipeline GitLab CI/CD configurado.

## Próximos Passos

Após a aprovação e merge da sua alteração, o pipeline aplicará automaticamente as modificações no Cloudflare.

