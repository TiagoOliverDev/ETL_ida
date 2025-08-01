from src.db.repositories.base import BaseRepository
from src.db.models import FatoIndicador

class FatoIdaRepository(BaseRepository):
    model = FatoIndicador

    def add_if_not_exists(self, id_tempo, id_grupo_economico, id_servico, id_variavel, valor):
        instance = (
            self.db_session.query(self.model)
            .filter_by(
                id_tempo=id_tempo,
                id_grupo_economico=id_grupo_economico,
                id_servico=id_servico,
                id_variavel=id_variavel
            )
            .first()
        )
        if instance:
            return instance
        instance = self.model(
            id_tempo=id_tempo,
            id_grupo_economico=id_grupo_economico,
            id_servico=id_servico,
            id_variavel=id_variavel,
            valor=valor
        )
        self.db_session.add(instance)
        self.db_session.flush()
        return instance
