variable "dns_records" {
  description = "Lista de registros DNS a serem criados"
  type = list(object({
    name        = string
    type        = string
    value       = string
    ttl         = number
    proxied     = bool
    comment     = optional(string, "Registro gerenciado pelo Terraform")
    settings    = optional(map(bool), {})
    owner       = string
    environment = string
    priority    = optional(number)  # Novo campo adicionado
  }))
}

variable "cloudflare_zone_id" {
  type        = string
  description = "ID da zona DNS no Cloudflare"
}

variable "cloudflare_api_token" {
  type        = string
  description = "API Token do Cloudflare"
}
