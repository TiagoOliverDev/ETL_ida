from src.db.models import DimVariavel
from src.db.repositories.base import BaseRepository

class DimVariavelRepository(BaseRepository):
    model = DimVariavel

    def get_or_create(self, nome_variavel: str):
        instance = self.db_session.query(self.model).filter_by(
            nome_variavel=nome_variavel
        ).first()
        if instance:
            return instance
        instance = self.model(nome_variavel=nome_variavel)
        self.db_session.add(instance)
        self.db_session.flush()
        return instance
