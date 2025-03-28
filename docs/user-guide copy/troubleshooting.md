# Solução de Problemas (Troubleshooting)

Este documento apresenta soluções para problemas comuns encontrados na automação de DNS com Terraform, Terragrunt e Cloudflare na RNP.

---

## 🚨 Erros Comuns e Como Resolver

### 1. ❌ Erro: `Error 403: Authentication error`

**Causa:**
- O token de API do Cloudflare pode estar incorreto ou sem permissões adequadas.
- A variável `TF_VAR_cloudflare_api_token` pode não estar definida no GitLab CI/CD.

**Solução:**
1. Verifique se a variável `TF_VAR_cloudflare_api_token` está configurada corretamente no GitLab CI/CD (**Settings > CI/CD > Variables**).
2. Confirme que o token de API tem as permissões adequadas (`Zone.DNS`, `Zone.Read`, `Zone.Settings.Read`).
3. Gere um novo token no Cloudflare e atualize no GitLab.

---

### 2. ❌ Erro: `Error 404: Zone not found`

**Causa:**
- O ID da zona Cloudflare pode estar incorreto.
- A variável `TF_VAR_cloudflare_zone_id` pode não estar definida.

**Solução:**
1. Confirme o ID da zona no Cloudflare.
2. Verifique se a variável `TF_VAR_cloudflare_zone_id` está configurada corretamente no GitLab CI/CD.
3. Atualize a variável e reinicie o pipeline.

---

### 3. ❌ Erro: `No changes. Infrastructure up-to-date.`

**Causa:**
- As alterações não foram corretamente aplicadas nos arquivos `terragrunt.hcl`.
- O merge request não contém mudanças relevantes para o Terraform aplicar.

**Solução:**
1. Verifique se o arquivo `terragrunt.hcl` foi atualizado corretamente.
2. Certifique-se de que as novas entradas foram adicionadas na lista `dns_records`.
3. Confirme que a branch está atualizada com a versão mais recente do repositório.

---

### 4. ❌ Pipeline falhando no `terraform plan`

**Causa:**
- Sintaxe incorreta no `terragrunt.hcl`.
- Falta de alguma variável obrigatória.

**Solução:**
1. Valide manualmente o arquivo antes de subir a alteração:
   ```bash
   terragrunt validate
   ```
2. Verifique se todas as variáveis obrigatórias estão definidas no arquivo `terragrunt.hcl`.
3. Confirme que a sintaxe do HCL está correta.

---

### 5. ❌ Registros DNS não estão aparecendo no Cloudflare

**Causa:**
- O pipeline pode não ter aplicado corretamente as mudanças.
- O merge request pode não ter sido aprovado e integrado.

**Solução:**
1. Verifique o log da pipeline no GitLab.
2. Confirme se o merge request foi aprovado e mesclado na branch principal.
3. Se necessário, force a reexecução da pipeline.

```bash
git commit --allow-empty -m "chore: reexecutando pipeline"
git push origin nome-da-branch
```

---

## 📌 Dicas para Evitar Problemas

✅ Sempre valide arquivos Terraform/Terragrunt antes de abrir um Merge Request:
```bash
terragrunt validate
```
✅ Verifique as permissões do token de API do Cloudflare.
✅ Confirme que todas as variáveis no GitLab CI/CD estão corretamente configuradas.
✅ Use o padrão Conventional Commits para facilitar o rastreamento das mudanças.

---

Seguindo essas diretrizes, a automação do DNS será mais eficiente e com menos erros!

