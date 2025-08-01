from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class DimTempo(Base):
    __tablename__ = 'dim_tempo'

    id_tempo = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    mes_ano = Column(String(7), nullable=False)

    fatos = relationship("FatoIda", back_populates="tempo")


class DimGrupoEconomico(Base):
    __tablename__ = 'dim_grupo_economico'

    id_grupo_economico = Column(Integer, primary_key=True, autoincrement=True)
    nome_grupo = Column(String(255), nullable=False)

    fatos = relationship("FatoIda", back_populates="grupo_economico")


class DimServico(Base):
    __tablename__ = 'dim_servico'

    id_servico = Column(Integer, primary_key=True, autoincrement=True)
    nome_servico = Column(String(50), nullable=False)

    fatos = relationship("FatoIda", back_populates="servico")


class FatoIda(Base):
    __tablename__ = 'fato_ida'

    id_fato = Column(Integer, primary_key=True, autoincrement=True)
    id_tempo = Column(Integer, ForeignKey('dim_tempo.id_tempo'), nullable=False)
    id_grupo_economico = Column(Integer, ForeignKey('dim_grupo_economico.id_grupo_economico'), nullable=False)
    id_servico = Column(Integer, ForeignKey('dim_servico.id_servico'), nullable=False)
    valor_ida = Column(Float, nullable=False)

    tempo = relationship("DimTempo", back_populates="fatos")
    grupo_economico = relationship("DimGrupoEconomico", back_populates="fatos")
    servico = relationship("DimServico", back_populates="fatos")
