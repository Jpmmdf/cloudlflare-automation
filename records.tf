resource "cloudflare_dns_record" "example_dns_record" {
  zone_id = cloudflare_zone.domain_zone.id
  comment = "Domain verification record"
  content = "198.51.100.4"
  name = "demo1.jcloud.com"
  proxied = true
  settings = {
    ipv4_only = true
    ipv6_only = true
  }
  tags = ["owner:dns-team"]
  ttl = 3600
  type = "A"
}