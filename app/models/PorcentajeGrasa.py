from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.shared.config.db import Base
from app.models.GeneroEnum import GeneroEnum  # Importa el Enum de género

class PorcentajeGrasa(Base):
    __tablename__ = "porcentaje_grasa"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    genero = Column(Enum(GeneroEnum), nullable=False)  # Usa el Enum GeneroEnum
    altura = Column(Float, nullable=False)
    cintura = Column(Float, nullable=False)
    resultado = Column(Float, nullable=True)  # Resultado será calculado

    usuario = relationship("User", back_populates="porcentajes_grasa")
