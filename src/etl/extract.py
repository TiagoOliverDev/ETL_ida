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
    """
        Realiza o download de um arquivo no formato ODS a partir de uma URL específica
        e salva o arquivo localmente na pasta configurada RAW_DIR com nome padronizado.

        Parâmetros:
        - service_key (str): identificador do serviço (ex: 'smp', 'stfc', 'scm') usado para nomear o arquivo.
        - url (str): URL direta do arquivo ODS a ser baixado.

        Retorna:
        - str: caminho completo do arquivo salvo localmente.
    """
    filename = RAW_DIR / f"ida_{service_key}.ods"
    
    logger.info(f"[INFO] Baixando {service_key.upper()} de {url}")
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as f:
        f.write(response.content)
    
    logger.info(f"[OK] Arquivo salvo em {filename}")
    return str(filename)

def run_extraction():
    """
        Itera sobre os links definidos no dicionário URLS, realizando o download dos arquivos ODS
        para cada serviço definido. Registra logs de sucesso e erros durante o processo.

        Retorna:
        - List[str]: lista de caminhos dos arquivos que foram baixados com sucesso.

        Em caso de falha no download de algum arquivo, captura e registra o erro, mas continua o processamento.
    """
    baixados = []
    for service, url in URLS.items():
        try:
            caminho = download_ods(service, url)
            baixados.append(caminho)
        except Exception as e:
            logger.error(f"[ERRO] Falha ao baixar {service.upper()}: {e}")
    return baixados
