from pathlib import Path
from etl.extract import run_extraction
from etl.transform import transform_and_filter_ods_to_csv
from etl.load import load_csv_to_db
from src.utils.logger import logger

def executar_etl_main():
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
