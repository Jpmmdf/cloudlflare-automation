variable "cloudflare_api_key" {}
variable "cloudflare_account_id" {}
variable "cf_domain" {
  default = "jcloud.com.br"
  type    = string
}

variable "cloudflare_zone_id" {}