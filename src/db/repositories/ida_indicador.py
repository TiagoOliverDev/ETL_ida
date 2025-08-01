from src.db.models import IdaIndicador
from src.db.repositories.base import BaseRepository

class IdaIndicadorRepository(BaseRepository[IdaIndicador]):
    def __init__(self):
        super().__init__(IdaIndicador)

    # aqui você pode adicionar métodos customizados, ex:
    def listar_por_grupo(self, db, grupo: str):
        return db.query(self.model).filter(self.model.grupo_economico == grupo).all()
