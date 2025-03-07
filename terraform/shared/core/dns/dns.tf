resource "cloudflare_dns_record" "dns_records" {
  for_each = {
    for record in var.dns_records :
    "${record.name}_${record.type}_${record.value}" => record
  }

  zone_id  = var.cloudflare_zone_id
  name     = each.value.name
  type     = each.value.type
  content  = each.value.value
  ttl      = each.value.ttl
  proxied  = each.value.proxied
  comment  = each.value.comment
  settings = each.value.settings
  priority = each.value.type == "MX" ? each.value.priority : null

}
