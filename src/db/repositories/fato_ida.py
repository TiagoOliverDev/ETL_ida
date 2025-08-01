from src.db.repositories.base import BaseRepository
from src.db.models import FatoIda

class FatoIdaRepository(BaseRepository):
    model = FatoIda

    def add_if_not_exists(self, id_tempo, id_grupo_economico, id_servico, valor_ida):
        instance = (
            self.db_session.query(self.model)
            .filter_by(
                id_tempo=id_tempo,
                id_grupo_economico=id_grupo_economico,
                id_servico=id_servico
            )
            .first()
        )
        if instance:
            return instance
        instance = self.model(
            id_tempo=id_tempo,
            id_grupo_economico=id_grupo_economico,
            id_servico=id_servico,
            valor_ida=valor_ida
        )
        self.db_session.add(instance)
        self.db_session.flush()
        return instance
