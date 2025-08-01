from src.db.repositories.base import BaseRepository
from src.db.models import DimServico

class DimServicoRepository(BaseRepository):
    model = DimServico

    def get_or_create(self, nome_servico: str):
        instance = self.db_session.query(self.model).filter_by(nome_servico=nome_servico).first()
        if instance:
            return instance
        instance = self.model(nome_servico=nome_servico)
        self.db_session.add(instance)
        self.db_session.flush()
        return instance