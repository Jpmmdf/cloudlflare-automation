# terragrunt.hcl

terraform {
  source = "../"
}

inputs = {
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
