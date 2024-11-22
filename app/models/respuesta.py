from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.shared.config.db import Base

class Respuesta(Base):
    __tablename__ = "respuesta"

    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    pregunta_id = Column(Integer, ForeignKey("pregunta.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("User", back_populates="respuestas")
    pregunta = relationship("Question", back_populates="respuestas")
