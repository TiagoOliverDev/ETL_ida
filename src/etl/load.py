import pandas as pd
from src.db.repositories.dim_tempo import DimTempoRepository
from src.db.repositories.dim_grupo_economico import DimGrupoEconomicoRepository
from src.db.repositories.dim_servico import DimServicoRepository
from src.db.repositories.fato_ida import FatoIdaRepository
from src.db.repositories.dim_variavel import DimVariavelRepository
from src.db.models import DimTempo, DimServico, DimGrupoEconomico, FatoIndicador, DimVariavel
from src.db.database import connect_db_sqlalchemy, get_session
from src.utils.logger import logger

MESES_MAP = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
}

def load_csv_to_db(csv_path):
    """
        Realiza a carga dos dados de um arquivo CSV para o banco de dados, populando as tabelas
        dimensionais e a tabela fato seguindo o modelo estrela.

        Passos principais:
        1. Conecta ao banco de dados via SQLAlchemy e inicia uma sessão.
        2. Inicializa os repositórios responsáveis por cada dimensão e a tabela fato.
        3. Lê o CSV com encoding Latin1 para manter compatibilidade com dados em português.
        4. Identifica colunas fixas (metadados) e colunas de meses (valores mensais).
        5. Para cada linha do dataframe:
        - Extrai e limpa os valores das dimensões: grupo econômico, variável e tipo de serviço.
        - Para cada coluna mensal, extrai o valor e ignora valores nulos.
        - Converte o nome do mês para número usando um mapeamento, e converte ano para inteiro.
        - Valida mês, registrando warning em caso de valores inválidos.
        - Obtém ou cria entradas nas tabelas dimensionais: tempo, grupo econômico, serviço e variável.
        - Insere a métrica (valor) na tabela fato se ainda não existir, evitando duplicidade.
        6. Finaliza a transação com commit e fecha a sessão.
        7. Loga sucesso do carregamento com o caminho do arquivo CSV.

        Parâmetros:
        - csv_path (str ou Path): caminho do arquivo CSV a ser carregado.

    """
    engine = connect_db_sqlalchemy()
    db_session = get_session(engine)

    tempo_repo = DimTempoRepository(db_session, DimTempo)
    grupo_repo = DimGrupoEconomicoRepository(db_session, DimGrupoEconomico)
    servico_repo = DimServicoRepository(db_session, DimServico)
    fato_repo = FatoIdaRepository(db_session, FatoIndicador)
    variavel_repo = DimVariavelRepository(db_session, DimVariavel)

    df = pd.read_csv(csv_path, encoding="latin1")

    # Colunas fixas
    colunas_fixas = ["grupo_economico", "variavel", "tipo_servico"]
    colunas_meses = [c for c in df.columns if c not in colunas_fixas]

    for _, row in df.iterrows():
        grupo_nome = row["grupo_economico"].strip()
        variavel_nome = row["variavel"].strip()
        servico_nome = row["tipo_servico"].strip()

        for mes_ano_col in colunas_meses:
            valor = row[mes_ano_col]
            if pd.isna(valor):
                continue

            try:
                mes_str, ano_str = mes_ano_col.split("_")
                mes = MESES_MAP.get(mes_str.lower())
                ano = int(ano_str)
                if mes is None:
                    logger.warning(f"Mes inválido: {mes_str} na linha {_}")
                    continue
            except Exception as e:
                logger.error(f"Erro ao processar coluna '{mes_ano_col}' na linha {_}: {e}")
                continue

            dim_tempo = tempo_repo.get_or_create(ano=ano, mes=mes, mes_ano=f"{ano}-{mes:02d}")
            dim_grupo = grupo_repo.get_or_create(nome_grupo=grupo_nome)
            dim_servico = servico_repo.get_or_create(nome_servico=servico_nome.upper())
            dim_variavel = variavel_repo.get_or_create(nome_variavel=variavel_nome)

            fato_repo.add_if_not_exists(
                id_tempo=dim_tempo.id_tempo,
                id_grupo_economico=dim_grupo.id_grupo_economico,
                id_servico=dim_servico.id_servico,
                id_variavel=dim_variavel.id_variavel,
                valor=float(valor)
            )

    db_session.commit()
    db_session.close()
    logger.info(f"[LOAD] Dados carregados com sucesso do arquivo {csv_path}")
