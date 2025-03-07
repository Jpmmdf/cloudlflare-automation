# terragrunt.hcl

terraform {
  source = "${get_repo_root()}/terraform/shared/core/dns"
}

include "root" {
  path = find_in_parent_folders("root.hcl")
}

inputs = {
  dns_records = [
    {
      name        = "demo"
      type        = "A"
      value       = "192.168.1.5"
      ttl         = 1
      proxied     = false
      comment     = "Criado pelo Terraform"
      settings    = {}
      owner       = "xpto"
      environment = "production"
    }
  ]
}