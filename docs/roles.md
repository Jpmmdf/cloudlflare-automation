# 📌 Role IAM para Remote State no Terragrunt

## 🎯 Visão Geral
Esta documentação descreve a role IAM criada para permitir que o **Terragrunt/Terraform** utilize o **S3 como backend** para armazenar o state e o **DynamoDB para locking**. A role segue o princípio de **mínimos privilégios**, garantindo apenas as permissões essenciais.

---

## 📂 Estrutura da Role

- **Nome da Role:** `TerraformRemoteStateRole`
- **Serviço Utilizado:** `AWS IAM`
- **Usuários/Serviços que utilizam:** `Terraform / Terragrunt`
- **Recursos acessados:**
  - **S3:** `terraform-state-bucket`
  - **DynamoDB:** `terraform-locks`

---

## 🔐 Permissões IAM

A role concede permissões mínimas para:

- **Armazenar e recuperar o Terraform state no S3**.
- **Criar, verificar e remover locks no DynamoDB**.

### 📜 Política IAM
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
				"s3:GetObject",
				"s3:PutObject",
				"s3:ListBucket",
				"s3:GetBucketPolicy",
				"s3:GetBucketVersioning",
				"s3:GetEncryptionConfiguration",
				"s3:GetBucketPublicAccessBlock",
				"s3:GetBucketAcl",
				"s3:PutBucketPolicy",
				"s3:PutBucketVersioning",
				"s3:PutEncryptionConfiguration",
				"s3:PutBucketPublicAccessBlock",
				"s3:ListBucketVersions"
            ],
            "Resource": [
                "arn:aws:s3:::SEU_BUCKET_TERRAFORM_STATE",
                "arn:aws:s3:::SEU_BUCKET_TERRAFORM_STATE/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:DeleteItem",
                "dynamodb:DescribeTable"
            ],
            "Resource": "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/NOME_DA_TABELA_DYNAMODB"
        }
    ]
}
```

---

## 📖 Como Usar

1. **Criar a política IAM**:
   - Acesse **IAM** → **Políticas** → **Criar Política**.
   - Selecione a aba **JSON** e cole a política acima.
   - Salve com o nome `TerraformRemoteStatePolicy`.

2. **Criar a Role IAM**:
   - Acesse **IAM** → **Funções** → **Criar Role**.
   - Escolha **AWS Service** → **EC2 ou Usuário IAM** (conforme necessário).
   - Anexe a política `TerraformRemoteStatePolicy`.

3. **Associar a Role ao Usuário/Serviço**:
   - Vá até **IAM** → **Usuários**.
   - Selecione o usuário que executa o Terraform/Terragrunt.
   - Anexe a Role recém-criada.

---

## ⚙️ Configuração no Terragrunt
No arquivo `terragrunt.hcl`, configure o backend conforme abaixo:

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

---

## 🛠️ Troubleshooting

### ❌ Erro `AccessDeniedException` no DynamoDB
- Se ocorrer o erro `dynamodb:DescribeTable`, certifique-se de que a permissão `dynamodb:DescribeTable` está incluída na política.

### ❌ Erro de permissão no S3
- Verifique se o bucket **terraform-state-bucket** realmente existe e que a role tem acesso a ele.

---

## 🔎 Referências
- [Documentação do Terraform Backend S3](https://developer.hashicorp.com/terraform/language/settings/backends/s3)
- [Documentação AWS IAM](https://docs.aws.amazon.com/iam/)

---

## 🏆 Conclusão
Com essa role, seu **Terraform/Terragrunt** terá apenas as permissões essenciais para armazenar o `terraform.tfstate` no S3 e usar o DynamoDB para locks, garantindo segurança e controle de concorrência no ambiente. 🚀

