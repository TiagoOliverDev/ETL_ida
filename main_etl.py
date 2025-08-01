from pathlib import Path
from src.etl.extract import run_extraction
from src.etl.transform import transform_and_filter_ods_to_csv
from src.etl.load import load_csv_to_db

def executar_etl_main():
    arquivos = run_extraction()
    for ods_path_str in arquivos:
        ods_path = Path(ods_path_str)
        servico = ods_path.stem.split("_")[-1]  # ex: ida_smp -> smp

        # Transformação + filtro direto do ODS para CSV final
        output_csv = transform_and_filter_ods_to_csv(ods_path, servico)
        print(f"[ETL] CSV gerado: {output_csv}")

        # # Chama o load para inserir no banco
        # load_csv_to_db(output_csv)
        # print(f"[ETL] Dados carregados no banco para o serviço {servico}")

if __name__ == "__main__":
    executar_etl_main()
