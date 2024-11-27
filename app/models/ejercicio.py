from sqlalchemy import Column, Integer, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class Ejercicio(Base):
    __tablename__ = 'ejercicio'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(Text, nullable=False)
    resumen = Column(Text, nullable=False)
    nivel_id = Column(Integer, ForeignKey('nivel_ejercicio.id', ondelete="CASCADE"), nullable=False)
    tiempo_descanso = Column(Integer, nullable=False)
    repeticiones = Column(Integer, nullable=False)
    imagen = Column(LargeBinary, nullable=True)
    ubicacion_id = Column(Integer, ForeignKey('ubicaciones.id', ondelete="CASCADE"), nullable=False)

    # Relaciones con otros modelos
    nivel = relationship("NivelEjercicio", back_populates="ejercicios")
    ubicacion = relationship("Ubicaciones", back_populates="ejercicios")
