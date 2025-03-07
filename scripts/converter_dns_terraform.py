import os
import json
import requests
import logging
from dotenv import load_dotenv
from typing import List, Dict, Any

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar variáveis de ambiente do .env
load_dotenv()

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
if not CLOUDFLARE_API_TOKEN:
    logging.error("CLOUDFLARE_API_TOKEN não configurado nas variáveis de ambiente.")
    exit(1)

CLOUDFLARE_BASE_URL = "https://api.cloudflare.com/client/v4"

# Diretório base do Terraform + Terragrunt
BASE_DIR = "terraform/xpto_account"

# Sessão para as requisições HTTP (para reaproveitar conexões)
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
})


# ------------------------------------------------------
# Funções para consumir API do Cloudflare
# ------------------------------------------------------

def get_zones() -> List[Dict[str, Any]]:
    """Obtém todas as zonas da conta Cloudflare."""
    logging.info("Buscando todas as zonas do Cloudflare...")
    url = f"{CLOUDFLARE_BASE_URL}/zones"
    response = session.get(url)
    response.raise_for_status()
    zones = response.json().get("result", [])
    logging.info(f"{len(zones)} zonas encontradas.")
    return zones

def get_dns_records(zone_id: str) -> List[Dict[str, Any]]:
    """Obtém todos os registros DNS de uma zona específica."""
    logging.info(f"Buscando registros DNS para a zona {zone_id}...")
    url = f"{CLOUDFLARE_BASE_URL}/zones/{zone_id}/dns_records"
    response = session.get(url)
    response.raise_for_status()
    records = response.json().get("result", [])
    logging.info(f"{len(records)} registros DNS encontrados para a zona {zone_id}.")
    return records


# ------------------------------------------------------
# Lógica de subpaths (subdomínios)
# ------------------------------------------------------

def get_subpath(record_name: str, zone_name: str) -> str:
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

def format_record_hcl(record: Dict[str, Any]) -> str:
    """
    Constrói o trecho HCL para cada item do 'dns_records'.
    Ajuste as chaves conforme sua estrutura.
    """
    # Usa "content" se existir, senão "value"
    record_value = record.get("content", record.get("value", ""))
    comment = record.get("comment", "Importado")
    proxied = record.get("proxied", False)
    ttl = record.get("ttl", 120)
    owner = record.get("owner", "auto-import")
    environment = record.get("environment", "production")

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

def generate_terragrunt_file(zone_name: str, zone_id: str, subpath: str, records: List[Dict[str, Any]]) -> None:
    """
    Cria um arquivo terragrunt.hcl (root module) em 'BASE_DIR/zone_name/dns/subpath/terragrunt.hcl'.
    """
    folder_path = os.path.join(BASE_DIR, zone_name, "dns", subpath)
    os.makedirs(folder_path, exist_ok=True)

    # Monta o array 'dns_records' em formato HCL
    record_blocks = [format_record_hcl(r) for r in records]
    joined_records = ",\n".join(record_blocks)

    terragrunt_content = f"""terraform {{
  source = "${{get_repo_root()}}/terraform/shared/core/dns"
}}

inputs = {{
  dns_records = [
{joined_records}
  ]
}}
"""
    terragrunt_path = os.path.join(folder_path, "terragrunt.hcl")
    try:
        with open(terragrunt_path, "w", encoding="utf-8") as f:
            f.write(terragrunt_content)
        logging.info(f"Arquivo gerado: {terragrunt_path}")
    except IOError as e:
        logging.error(f"Erro ao gerar o arquivo {terragrunt_path}: {e}")


# ------------------------------------------------------
# Função principal
# ------------------------------------------------------

def main() -> None:
    zones = get_zones()
    if not zones:
        logging.warning("Nenhuma zona encontrada.")
        return

    for zone in zones:
        zone_name = zone.get("name")
        zone_id = zone.get("id")
        if not zone_name or not zone_id:
            logging.warning("Zona com dados incompletos, pulando...")
            continue

        logging.info(f"Processando zona: {zone_name} ({zone_id})")
        dns_records = get_dns_records(zone_id)
        groups: Dict[str, List[Dict[str, Any]]] = {}

        # Agrupa os registros por subpath
        for record in dns_records:
            subpath = get_subpath(record.get("name", ""), zone_name)
            groups.setdefault(subpath, []).append(record)

        # Para cada subpath, gera um terragrunt.hcl
        for subpath, records in groups.items():
            generate_terragrunt_file(zone_name, zone_id, subpath, records)

    logging.info("Arquivos terragrunt.hcl gerados com sucesso!")

if __name__ == "__main__":
    main()
