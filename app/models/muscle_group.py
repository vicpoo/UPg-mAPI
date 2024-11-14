# muscle_group.py

from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class MuscleGroup(Base):
    __tablename__ = "grupomuscular"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    imagen = Column(LargeBinary, nullable=True)

    # Relación con Exercise
    ejercicios = relationship("Exercise", back_populates="grupo_muscular")
