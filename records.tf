resource "cloudflare_record" "any_record_a" {
  zone_id = cloudflare_zone.domain_zone.id
  name    = "demo1.jcloud.com.br"
  content = "198.51.100.45"
  type    = "A"
  proxied = true
}
