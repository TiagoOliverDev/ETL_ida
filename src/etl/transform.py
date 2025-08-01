import pandas as pd
from pathlib import Path
from src.utils.logger import logger
from src.utils.utils import convert_value_ida

MAPA_MESES = {
    "01": "janeiro", "02": "fevereiro", "03": "marco", "04": "abril",
    "05": "maio", "06": "junho", "07": "julho", "08": "agosto",
    "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"
}

def transform_and_filter_ods_to_csv(ods_path: Path, servico: str) -> Path:
    try:
        df_full = pd.read_excel(ods_path, engine="odf", header=None, dtype=str)
        logger.info(f"[TRANSFORM] ODS carregado com {len(df_full)} linhas")

        header = df_full.iloc[8].tolist()
        df = df_full.iloc[9:].reset_index(drop=True)
        df.columns = header

        # Renomeia as colunas que já existem
        df = df.rename(columns={
            "VARIÁVEL": "variavel",
            "GRUPO ECONÔMICO": "grupo_economico"
        })

        # Remove linhas inválidas
        df = df.dropna(subset=["grupo_economico", "variavel"])
        df = df[
            (df["grupo_economico"].str.strip() != "") &
            (df["variavel"].str.strip() != "")
        ]

        # Adiciona a coluna tipo_servico, que é nova
        df["tipo_servico"] = servico.upper()

        # Identifica colunas de valores no formato "AAAA-MM"
        colunas_valores = [col for col in df.columns if isinstance(col, str) and len(col) == 7 and col[:4].isdigit() and col[4] == "-"]

        for col in colunas_valores:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .apply(convert_value_ida)
            )

        # Renomeia as colunas de datas para formato "mes_ano"
        novas_colunas = {}
        for col in colunas_valores:
            ano, mes = col.split("-")
            mes_extenso = MAPA_MESES.get(mes.zfill(2))
            if mes_extenso:
                novas_colunas[col] = f"{mes_extenso}_{ano}"

        df = df.rename(columns=novas_colunas)

        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"ida_{servico.lower()}_final.csv"
        df.to_csv(output_file, index=False, encoding="latin1")
        logger.info(f"[TRANSFORM] CSV final salvo em {output_file}")

        return output_file

    except Exception as e:
        logger.error(f"[TRANSFORM] Erro no processamento do ODS {ods_path}: {e}")
        raise
