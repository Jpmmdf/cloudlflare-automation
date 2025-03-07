# Documentação do Script: Integração Cloudflare/Terragrunt

Este documento descreve o funcionamento, configuração e uso do script que integra a API do Cloudflare com a geração automática de arquivos `terragrunt.hcl`. O script utiliza dados das zonas e registros DNS do Cloudflare para organizar a infraestrutura do Terraform/Terragrunt de forma automatizada.

---

## Sumário

- [Visão Geral](#visao-geral)
- [Requisitos](#requisitos)
- [Instalação](#instalacao)
- [Configuração](#configuracao)
- [Uso](#uso)
- [Estrutura de Arquivos Gerados](#estrutura-de-arquivos-gerados)
- [Detalhes do Código](#detalhes-do-codigo)
- [Logs e Tratamento de Erros](#logs-e-tratamento-de-erros)
- [Personalizações](#personalizacoes)

---

## Visão Geral

O script realiza as seguintes operações:
- Conecta-se à API do Cloudflare para buscar todas as zonas configuradas.
- Para cada zona, obtém os registros DNS associados.
- Agrupa os registros com base no subdomínio (subpath), determinando se o registro pertence à zona raiz ou a um subdomínio específico.
- Gera um arquivo `terragrunt.hcl` para cada grupo de registros, configurando os inputs necessários para o Terraform/Terragrunt.  
- Utiliza a seguinte referência para o módulo Terraform:
  
  ```hcl
  terraform {
    source = "${get_repo_root()}/terraform/shared"
  }
  ```

---

## Requisitos

- **Python 3.6+**  
- **Pacotes Python:**
  - `requests`
  - `python-dotenv`

Instale as dependências usando:

```bash
pip install -r requirements.txt
```

ou

```bash
pip install requests python-dotenv
```

---

## Configuração

1. **Variáveis de Ambiente:**  
   Crie um arquivo `.env` e defina:

   ```dotenv
   CLOUDFLARE_API_TOKEN=seu_token_aqui
   ```

2. **Diretório Base:**  
   O diretório onde os arquivos `terragrunt.hcl` serão gerados pode ser configurado na variável `BASE_DIR` no script:

   ```python
   BASE_DIR = "terraform/xpto_account"
   ```

3. **Módulo Terraform:**  
   O script gera arquivos `terragrunt.hcl` que usam:

   ```hcl
   source = "${get_repo_root()}/terraform/shared"
   ```

   Ajuste conforme necessário.

---

## Uso

Execute o script com:

```bash
python converter_dns_terraform.py
```

Isso irá:
- Buscar as zonas e registros DNS do Cloudflare.
- Gerar os arquivos `terragrunt.hcl` organizados por zona e subpath.
- Exibir mensagens de log informando o progresso e eventuais erros.

---

## Estrutura de Arquivos Gerados

```
terraform/xpto_account/
├── <zone_name>/
│   └── dns/
│       ├── root/
│       │   └── terragrunt.hcl
│       └── <subpath>/
│           └── terragrunt.hcl
```

---

## Detalhes do Código

### Funções Principais

- **`get_zones()`** - Retorna todas as zonas do Cloudflare.
- **`get_dns_records(zone_id)`** - Retorna os registros DNS da zona especificada.
- **`get_subpath(record_name, zone_name)`** - Determina o subpath com base no nome do registro.
- **`format_record_hcl(record)`** - Formata um registro DNS no formato HCL.
- **`generate_terragrunt_file(zone_name, zone_id, subpath, records)`** - Gera o arquivo `terragrunt.hcl` correspondente.
- **`main()`** - Função principal que executa o fluxo completo.

---

## Logs e Tratamento de Erros

- **Logging:**  
  Usa `logging` para informar o progresso e erros.
- **Tratamento de Erros:**  
  - Verifica se `CLOUDFLARE_API_TOKEN` está configurado.
  - Utiliza `try/except` ao escrever arquivos para capturar erros de I/O.
  - Valida se os dados retornados da API contêm as chaves esperadas.

---

## Personalizações

- **Diretório Base (`BASE_DIR`)** - Altere para modificar o local de geração dos arquivos.
- **Fonte do Terraform (`source`)** - Modifique o caminho do módulo Terraform no `terragrunt.hcl`.
- **Formato dos Registros** - Ajuste `format_record_hcl(record)` para incluir mais atributos se necessário.

---

Este documento pode ser integrado ao [MkDocs](https://www.mkdocs.org/) para facilitar a documentação e manutenção do script.

