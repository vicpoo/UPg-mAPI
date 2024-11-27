from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class Ubicaciones(Base):
    __tablename__ = 'ubicaciones'

    id = Column(Integer, primary_key=True, index=True)
    ubicacion = Column(Text, nullable=False, unique=True)

    # Relación con el modelo Ejercicio
    ejercicios = relationship("Ejercicio", back_populates="ubicacion")
