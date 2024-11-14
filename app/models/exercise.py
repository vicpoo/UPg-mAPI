from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

# Definir los valores de Nivel y UbicacionEjercicio en SQLAlchemy directamente
class Exercise(Base):
    __tablename__ = "ejercicio"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    resumen = Column(String, nullable=True)
    nivel = Column(SQLEnum('BASICO', 'INTERMEDIO', 'AVANZADO', name="nivel"), nullable=False)
    tiempo_descanso = Column(Integer, nullable=True)
    repeticiones = Column(Integer, nullable=True)
    imagen = Column(LargeBinary, nullable=True)
    ubicacion = Column(SQLEnum('CASA', 'GYM', name="ubicacion_ejercicio"), nullable=False)
    grupo_muscular_id = Column(Integer, ForeignKey("grupomuscular.id"), nullable=True)

    # Relación con MuscleGroup
    grupo_muscular = relationship("MuscleGroup", back_populates="ejercicios")
