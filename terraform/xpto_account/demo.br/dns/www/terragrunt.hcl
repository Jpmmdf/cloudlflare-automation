# terragrunt.hcl

terraform {
  source = "../"
}

inputs = {
  dns_records = [
    {
      name        = "www"
      type        = "A"
      value       = "192.168.1.1"
      ttl         = 1
      proxied     = false
      comment     = "Criado pelo Terraform"
      settings    = {}
      owner       = "xpto"
      environment = "production"
    }
  ]
}
