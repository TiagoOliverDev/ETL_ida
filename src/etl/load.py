import pandas as pd
# from src.db.database import SessionLocal
from src.db.repositories.dim_tempo import DimTempoRepository
from src.db.repositories.dim_grupo_economico import DimGrupoEconomicoRepository
from src.db.repositories.dim_servico import DimServicoRepository
from src.db.repositories.fato_ida import FatoIdaRepository
from src.db.models import DimTempo, DimServico, DimGrupoEconomico, FatoIda
from src.db.database import connect_db_sqlalchemy, get_session

MESES_MAP = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
}

def load_csv_to_db(csv_path):
    engine = connect_db_sqlalchemy()
    db_session = get_session(engine)
    
    tempo_repo = DimTempoRepository(db_session, DimTempo)
    grupo_repo = DimGrupoEconomicoRepository(db_session, DimGrupoEconomico)
    servico_repo = DimServicoRepository(db_session, DimServico)
    fato_repo = FatoIdaRepository(db_session, FatoIda)

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        grupo_nome = row["grupo_economico"]
        # servico = row["variavel"]  # ou defina seu serviço de forma adequada
        servico = row["tipo_servico"]

        colunas_meses = [c for c in df.columns if c not in ["grupo_economico", "variavel", "tipo_servico"]]

        for mes_ano_col in colunas_meses:
            valor_ida = row[mes_ano_col]
            if pd.isna(valor_ida):
                continue

            mes_str, ano_str = mes_ano_col.split("_")
            ano = int(ano_str)
            mes = MESES_MAP.get(mes_str.lower())
            if mes is None:
                continue

            dim_tempo = tempo_repo.get_or_create(ano=ano, mes=mes, mes_ano=f"{ano}-{mes:02d}")
            dim_grupo = grupo_repo.get_or_create(nome_grupo=grupo_nome)
            dim_servico = servico_repo.get_or_create(nome_servico=servico.upper())

            fato_repo.add_if_not_exists(
                id_tempo=dim_tempo.id_tempo,
                id_grupo_economico=dim_grupo.id_grupo_economico,
                id_servico=dim_servico.id_servico,
                valor_ida=valor_ida
            )

    db_session.commit()
    db_session.close()
