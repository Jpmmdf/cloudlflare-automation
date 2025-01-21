resource "cloudflare_record" "any_record_a" {
  zone_id = cloudflare_zone.domain_zone.id
  name    = "demo1.jcloud.com"
  content = "198.51.100.4"
  type    = "A"
  proxied = true
}
