from src.db.models import DimTempo
from src.db.repositories.base import BaseRepository

class DimTempoRepository(BaseRepository):
    model = DimTempo

    def get_or_create(self, ano: int, mes: int, mes_ano: str):
        instance = self.db_session.query(self.model).filter_by(
            ano=ano, mes=mes, mes_ano=mes_ano
        ).first()
        if instance:
            return instance
        instance = self.model(ano=ano, mes=mes, mes_ano=mes_ano)
        self.db_session.add(instance)
        self.db_session.flush()
        return instance