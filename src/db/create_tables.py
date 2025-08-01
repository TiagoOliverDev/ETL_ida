import logging
from src.db.database import engine, Base
from src.db.models import DimTempo, DimGrupoEconomico, DimServico, DimVariavel, FatoIndicador

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso (ou já existiam).")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        raise

if __name__ == "__main__":
    create_tables()
