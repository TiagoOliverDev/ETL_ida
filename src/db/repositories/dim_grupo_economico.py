from src.db.repositories.base import BaseRepository
from src.db.models import DimGrupoEconomico

class DimGrupoEconomicoRepository(BaseRepository):
    model = DimGrupoEconomico

    def get_or_create(self, nome_grupo: str):
        instance = self.db_session.query(self.model).filter_by(nome_grupo=nome_grupo).first()
        if instance:
            return instance
        instance = self.model(nome_grupo=nome_grupo)
        self.db_session.add(instance)
        self.db_session.flush()  # para garantir que o id seja atribuído imediatamente
        return instance
