from pathlib import Path
from src.etl.extract import run_extraction
from src.etl.transform import transform_and_filter_ods_to_csv
from src.etl.load import load_csv_to_db
from src.utils.logger import logger

def executar_etl_main():
    """
        Executa o pipeline ETL completo:
        1. Baixa os arquivos ODS via run_extraction.
        2. Para cada arquivo baixado, transforma e filtra os dados para CSV.
        3. Carrega os dados do CSV no banco de dados.
        4. Registra logs para sucesso ou falha em cada etapa.
    """
    arquivos = run_extraction()
    for ods_path_str in arquivos:
        try:
            ods_path = Path(ods_path_str)
            servico = ods_path.stem.split("_")[-1]  

            output_csv = transform_and_filter_ods_to_csv(ods_path, servico)
            logger.info(f"✅ [ETL] CSV gerado: {output_csv}")
            
            load_csv_to_db(output_csv)
            logger.info(f"🚀 [ETL] Dados carregados no banco para o serviço {servico}")

        except Exception as e:
            logger.error(f"❌ [ETL] Erro no arquivo {ods_path_str}: {e}", exc_info=True)

if __name__ == "__main__":
    executar_etl_main()
