from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class NivelEjercicio(Base):
    __tablename__ = 'nivel_ejercicio'

    id = Column(Integer, primary_key=True, index=True)
    nivel = Column(Text, nullable=False, unique=True)

    # Relación con el modelo Ejercicio
    ejercicios = relationship("Ejercicio", back_populates="nivel")
