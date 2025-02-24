# terragrunt.hcl

terraform {
  source = "../"
}
locals {
  cf_api_token = get_env("CLOUDFLARE_API_TOKEN", "")
  cf_zone_id   = get_env("CLOUDFLARE_ZONE_ID", "")
}

inputs = {
  cloudflare_api_token = local.cf_api_token
  cloudflare_zone_id   = local.cf_zone_id
  dns_records = [
    {
      name        = "xpto"
      type        = "A"
      value       = "192.168.1.2"
      ttl         = 1
      proxied     = false
      comment     = "Criado pelo Terraform"
      settings    = {}
      owner       = "xpto"
      environment = "production"
    }
  ]
}