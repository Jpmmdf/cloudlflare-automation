resource "cloudflare_dns_record" "dns_records" {
  for_each = { for record in var.dns_records : record.name => record }

  zone_id  = var.cloudflare_zone_id
  comment  = each.value.comment
  content  = each.value.value
  name     = each.value.name
  proxied  = each.value.proxied
  ttl      = each.value.ttl
  type     = each.value.type

  settings = each.value.settings
# Somente na conta enterprise
#  tags = [
#    "owner:${each.value.owner}",
#    "environment:${each.value.environment}"
#  ]
}
