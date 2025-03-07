import os
import json
import requests
import logging
import subprocess
import shutil
from dotenv import load_dotenv
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_BASE_URL = "https://api.cloudflare.com/client/v4"
BASE_DIR = "terraform/xpto_account"

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
})

def get_zones() -> List[Dict[str, Any]]:
    url = f"{CLOUDFLARE_BASE_URL}/zones"
    response = session.get(url)
    response.raise_for_status()
    return response.json().get("result", [])

def get_dns_records(zone_id: str) -> List[Dict[str, Any]]:
    url = f"{CLOUDFLARE_BASE_URL}/zones/{zone_id}/dns_records"
    response = session.get(url)
    response.raise_for_status()
    return response.json().get("result", [])

def terraform_import(record: Dict[str, Any], zone_id: str, resource_name: str, working_base_dir: str):
    record_id = record["id"]
    cmd = [
        "terraform", "import", "-var-file=terraform.tfvars",
        f'cloudflare_dns_record.dns_records["{resource_name}"]',
        f"{zone_id}/{record_id}"
    ]

    terragrunt_cache_dir = None
    for root, dirs, files in os.walk(working_base_dir):
        if ".terragrunt-cache" in root and any(f.endswith(".tf") for f in files):
            terragrunt_cache_dir = root
            break

    if not terragrunt_cache_dir:
        logging.error(f"Nenhum diretório .terragrunt-cache encontrado em {working_base_dir}")
        return

    shutil.copy(os.path.join(working_base_dir, "terraform.tfvars"), terragrunt_cache_dir)

    logging.info(f"Executando terraform import em: {terragrunt_cache_dir}")
    subprocess.run(cmd, check=True, cwd=terragrunt_cache_dir)

def format_record_hcl(record: Dict[str, Any]) -> str:
    return json.dumps({
        "name": record["name"],
        "type": record["type"],
        "value": record["content"],
        "ttl": record.get("ttl", 120),
        "proxied": record.get("proxied", False),
        "comment": record.get("comment", "Importado"),
        "settings": {},
        "owner": "auto-import",
        "environment": "production"
    }, indent=2)

def get_subpath(record_name: str, zone_name: str) -> str:
    if record_name == zone_name:
        return "root"
    if record_name.endswith(f".{zone_name}"):
        subdomain = record_name[:-(len(zone_name) + 1)]
        return subdomain.replace('.', '/')
    return "others"

def generate_terragrunt_file(zone_name: str, zone_id: str, records: List[Dict[str, Any]]) -> None:
    groups = {}
    for record in records:
        subpath = get_subpath(record["name"], zone_name)
        groups.setdefault(subpath, []).append(record)

    for subpath, grouped_records in groups.items():
        folder_path = os.path.join(BASE_DIR, zone_name, "dns", subpath)
        os.makedirs(folder_path, exist_ok=True)

        record_blocks = [format_record_hcl(record) for record in grouped_records]

        terragrunt_content = f"""terraform {{
  source = "${{get_repo_root()}}/terraform/shared/core/dns"
}}

inputs = {{
  dns_records = [
{',\n'.join(record_blocks)}
  ]
}}
"""

        with open(os.path.join(folder_path, "terragrunt.hcl"), "w", encoding="utf-8") as f:
            f.write(terragrunt_content)

        terraform_tfvars_content = f"dns_records = [\n{',\n'.join(record_blocks)}\n]"
        tfvars_path = os.path.join(folder_path, "terraform.tfvars")

        with open(tfvars_path, "w", encoding="utf-8") as f:
            f.write(terraform_tfvars_content)

        for record in grouped_records:
            resource_key = f"{record['name']}_{record['type']}_{record['content']}"
            terraform_import(record, zone_id, resource_key, folder_path)

        logging.info(f"Terragrunt file criado em: {folder_path}")

def main() -> None:
    zones = get_zones()
    for zone in zones:
        zone_name, zone_id = zone["name"], zone["id"]
        records = get_dns_records(zone_id)
        generate_terragrunt_file(zone_name, zone_id, records)

if __name__ == "__main__":
    main()
