resource "cloudflare_record" "any_record_a" {
  zone_id = var.cloudflare_zone_id
  name    = "demo1.jcloud.com.br"
  content = "198.51.100.45"
  type    = "A"
  proxied = true
}
