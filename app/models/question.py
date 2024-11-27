from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.shared.config.db import Base
from app.models.User import User # Asegúrate de importar el modelo de usuario
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "pregunta"

    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with other models, such as answers (Respuesta)
    usuario = relationship("User", back_populates="questions")  # Relación con el modelo User

       # Relación con respuestas
    respuestas = relationship(
        "Respuesta",
        back_populates="pregunta",
        cascade="all, delete",  # Esto asegura la eliminación en cascada en SQLAlchemy
    )