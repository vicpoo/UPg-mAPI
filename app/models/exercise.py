# exercise.py

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class Exercise(Base):
    __tablename__ = "ejercicio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    grupo_muscular_id = Column(Integer, ForeignKey("grupomuscular.id"))
    imagen = Column(LargeBinary, nullable=True)

    # Relación con MuscleGroup
    grupo_muscular = relationship("MuscleGroup", back_populates="ejercicios")
