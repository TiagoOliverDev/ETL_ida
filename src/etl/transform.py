import pandas as pd
from pathlib import Path
from src.utils.logger import logger
from src.utils.utils import convert_value_ida

# Mapeamento de número de mês para nome em português
MAPA_MESES = {
    "01": "janeiro", "02": "fevereiro", "03": "marco", "04": "abril",
    "05": "maio", "06": "junho", "07": "julho", "08": "agosto",
    "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"
}

def transform_and_filter_ods_to_csv(ods_path: Path, servico: str) -> Path:
    """
    Lê o arquivo ODS, remove as 8 primeiras linhas, aplica o header correto da linha 9,
    filtra só 'Indicador de Desempenho no Atendimento (IDA)', normaliza colunas de valores,
    renomeia colunas e salva CSV final filtrado.
    """
    try:
        # Lê arquivo ODS completo, sem header, forçando leitura como string
        df_full = pd.read_excel(ods_path, engine="odf", header=None, dtype=str)
        logger.info(f"[TRANSFORM] ODS carregado com {len(df_full)} linhas")

        # Extrai header da linha 9 (índice 8)
        header = df_full.iloc[8].tolist()
        logger.info(f"[TRANSFORM] Header extraído: {header}")

        # Remove as 9 primeiras linhas (0-8)
        df = df_full.iloc[9:].reset_index(drop=True)

        # Aplica header como colunas
        df.columns = header

        # Filtra só linhas onde VARIÁVEL == 'Indicador de Desempenho no Atendimento (IDA)'
        df_ida = df[df["VARIÁVEL"] == "Indicador de Desempenho no Atendimento (IDA)"]
        logger.info(f"[TRANSFORM] Linhas após filtro IDA: {len(df_ida)}")
        df_ida["tipo_servico"] = servico.upper()

        # Normaliza os valores das colunas mensais
        colunas_valores = [col for col in df_ida.columns if isinstance(col, str) and col.startswith("20")]
        for col in colunas_valores:
            df_ida[col] = (
                df_ida[col]
                .astype(str)
                .str.strip()
                .str.replace(".", "", regex=False)  # Remove ponto de milhar
                .str.replace(",", ".", regex=False)  # Substitui vírgula decimal por ponto
            )
            df_ida[col] = df_ida[col].apply(convert_value_ida)

        # Renomeia colunas principais
        df_ida = df_ida.rename(columns={
            "VARIÁVEL": "variavel",
            "GRUPO ECONÔMICO": "grupo_economico"
        })

        # Renomeia colunas de mês/ano
        novas_colunas = {}
        for col in colunas_valores:
            ano, mes = col.split("-")
            mes_extenso = MAPA_MESES.get(mes)
            if mes_extenso:
                novas_colunas[col] = f"{mes_extenso}_{ano}"

        df_ida = df_ida.rename(columns=novas_colunas)

        # Salva CSV final filtrado
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"ida_{servico.lower()}_final.csv"
        df_ida.to_csv(output_file, index=False)
        logger.info(f"[TRANSFORM] CSV final salvo em {output_file}")

        return output_file

    except Exception as e:
        logger.error(f"[TRANSFORM] Erro no processamento do ODS {ods_path}: {e}")
        raise


