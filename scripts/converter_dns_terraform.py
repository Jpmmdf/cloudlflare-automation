import os
import json
import requests
import logging
from dotenv import load_dotenv

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar variáveis de ambiente do .env
load_dotenv()

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_BASE_URL = "https://api.cloudflare.com/client/v4"

# Diretório base do Terraform + Terragrunt
BASE_DIR = "terraform/xpto_account"

# ------------------------------------------------------
# Funções para consumir API do Cloudflare
# ------------------------------------------------------

def get_zones():
    """Obtém todas as zonas da conta Cloudflare."""
    logging.info("Buscando todas as zonas do Cloudflare...")
    url = f"{CLOUDFLARE_BASE_URL}/zones"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    zones = response.json()["result"]
    logging.info(f"{len(zones)} zonas encontradas.")
    return zones

def get_dns_records(zone_id):
    """Obtém todos os registros DNS de uma zona específica."""
    logging.info(f"Buscando registros DNS para a zona {zone_id}...")
    url = f"{CLOUDFLARE_BASE_URL}/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    records = response.json()["result"]
    logging.info(f"{len(records)} registros DNS encontrados para a zona {zone_id}.")
    return records

# ------------------------------------------------------
# Lógica de subpaths (subdomínios)
# ------------------------------------------------------

def get_subpath(record_name, zone_name):
    """
    Retorna o caminho relativo (subpath) a partir do nome do registro,
    removendo o domínio (zona). Caso o registro seja a zona raiz, retorna "root".
    """
    if record_name == zone_name:
        return "root"
    if record_name.endswith("." + zone_name):
        # Ex.: api.teste.zone.com => subpath 'api/teste'
        subdomain = record_name[:-len(zone_name)-1]
        return os.path.join(*subdomain.split("."))
    return "others"

# ------------------------------------------------------
# Geração do arquivo terragrunt.hcl
# ------------------------------------------------------

def format_record_hcl(record):
    """
    Constrói o trecho HCL para cada item do 'dns_records'.
    Ajuste as chaves conforme sua estrutura.
    """
    # Usa "content" se existir, senão "value"
    record_value = record.get("content", record.get("value", ""))
    comment = record.get("comment", "Importado")
    # Se 'proxied' não existir, por padrão define False
    proxied = record.get("proxied", False)
    ttl = record.get("ttl", 120)
    owner = record.get("owner", "auto-import")
    environment = record.get("environment", "production")

    # Monta string HCL do objeto no array `dns_records`
    return f"""
    {{
      name        = "{record["name"]}"
      type        = "{record["type"]}"
      value       = "{record_value}"
      ttl         = {ttl}
      proxied     = {str(proxied).lower()}
      comment     = "{comment}"
      settings    = {{}}
      owner       = "{owner}"
      environment = "{environment}"
    }}"""

def generate_terragrunt_file(zone_name, zone_id, subpath, records):
    """
    Cria um arquivo terragrunt.hcl (um root module) em 'BASE_DIR/zone_name/dns/subpath/terragrunt.hcl'.
    """
    folder_path = os.path.join(BASE_DIR, zone_name, "dns", subpath)
    os.makedirs(folder_path, exist_ok=True)

    # Monta o array 'dns_records' em formato HCL
    record_blocks = [format_record_hcl(r) for r in records]
    joined_records = ",\n".join(record_blocks)

    # Exemplo de Terragrunt com "locals" e "inputs"
    # Observação: zone_id poderia vir do get_env no terragrunt.hcl, mas aqui está para simplificar.
    terragrunt_content = f"""terraform {{
  source = "../../../../modules/dns"
}}

inputs = {{

  dns_records = [
{joined_records}
  ]
}}
"""

    terragrunt_path = os.path.join(folder_path, "terragrunt.hcl")
    logging.info(f"Gerando {terragrunt_path}")
    with open(terragrunt_path, "w") as f:
        f.write(terragrunt_content)

# ------------------------------------------------------
# MAIN - Execução
# ------------------------------------------------------

if __name__ == "__main__":
    zones = get_zones()
    if not zones:
        logging.warning("Nenhuma zona encontrada.")
        exit(0)

    for zone in zones:
        zone_name = zone["name"]
        zone_id = zone["id"]
        logging.info(f"Processando zona: {zone_name} ({zone_id})")

        dns_records = get_dns_records(zone_id)
        # Agrupa os registros por subpath
        groups = {}
        for record in dns_records:
            subpath = get_subpath(record["name"], zone_name)
            groups.setdefault(subpath, []).append(record)

        # Para cada subpath, gera um terragrunt.hcl
        for subpath, records in groups.items():
            generate_terragrunt_file(zone_name, zone_id, subpath, records)

    logging.info("Arquivos terragrunt.hcl gerados com sucesso!")
