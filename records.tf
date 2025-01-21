resource "cloudflare_record" "any_record_a" {
  zone_id = cloudflare_zone.jcloud_zone.id
  name    = "demo1.jcloud.com.br"
  content = "198.51.100.15"
  type    = "A"
  proxied = true
}


resource "cloudflare_record" "any_record_b" {
  zone_id = cloudflare_zone.jcloud_zone.id
  name    = "demo2.jcloud.com.br"
  content = "198.51.100.22"
  type    = "A"
  proxied = true
}

