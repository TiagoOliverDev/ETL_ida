from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base


class DimVariavel(Base):
    __tablename__ = 'dim_variavel'

    id_variavel = Column(Integer, primary_key=True, autoincrement=True)
    nome_variavel = Column(String(255), nullable=False)

    fatos = relationship("FatoIndicador", back_populates="variavel")


class DimTempo(Base):
    __tablename__ = 'dim_tempo'

    id_tempo = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    mes_ano = Column(String(7), nullable=False)

    fatos = relationship("FatoIndicador", back_populates="tempo")


class DimGrupoEconomico(Base):
    __tablename__ = 'dim_grupo_economico'

    id_grupo_economico = Column(Integer, primary_key=True, autoincrement=True)
    nome_grupo = Column(String(255), nullable=False)

    fatos = relationship("FatoIndicador", back_populates="grupo_economico")


class DimServico(Base):
    __tablename__ = 'dim_servico'

    id_servico = Column(Integer, primary_key=True, autoincrement=True)
    nome_servico = Column(String(50), nullable=False)

    fatos = relationship("FatoIndicador", back_populates="servico")


class FatoIndicador(Base):
    __tablename__ = 'fato_indicador'

    id_fato = Column(Integer, primary_key=True, autoincrement=True)
    id_tempo = Column(Integer, ForeignKey('dim_tempo.id_tempo'), nullable=False)
    id_grupo_economico = Column(Integer, ForeignKey('dim_grupo_economico.id_grupo_economico'), nullable=False)
    id_servico = Column(Integer, ForeignKey('dim_servico.id_servico'), nullable=False)
    id_variavel = Column(Integer, ForeignKey('dim_variavel.id_variavel'), nullable=False)
    valor = Column(Float, nullable=False)

    tempo = relationship("DimTempo", back_populates="fatos")
    grupo_economico = relationship("DimGrupoEconomico", back_populates="fatos")
    servico = relationship("DimServico", back_populates="fatos")
    variavel = relationship("DimVariavel", back_populates="fatos")
