import requests
from config.settings import RAW_DIR
from src.utils.logger import logger

# Links diretos .ods hospedados pela Anatel
URLS = {
    "smp": "https://www.anatel.gov.br/dadosabertos/PDA/IDA/SMP2019.ods",
    "stfc": "https://www.anatel.gov.br/dadosabertos/PDA/IDA/STFC2019.ods",
    "scm": "https://www.anatel.gov.br/dadosabertos/PDA/IDA/SCM2019.ods"
}


def download_ods(service_key: str, url: str) -> str:
    """Faz o download de um ODS e salva em data/raw"""
    filename = RAW_DIR / f"ida_{service_key}.ods"
    
    print(f"[INFO] Baixando {service_key.upper()} de {url}")
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as f:
        f.write(response.content)
    
    print(f"[OK] Arquivo salvo em {filename}")
    return str(filename)

def run_extraction():
    baixados = []
    for service, url in URLS.items():
        try:
            caminho = download_ods(service, url)
            baixados.append(caminho)
        except Exception as e:
            print(f"[ERRO] Falha ao baixar {service.upper()}: {e}")
    return baixados
