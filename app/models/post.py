from sqlalchemy import Column, Integer, Text, LargeBinary, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.shared.config.db import Base

class Post(Base):
    __tablename__ = "publicacion"

    id = Column(Integer, primary_key=True)
    descripcion = Column(Text, nullable=False)
    imagen = Column(LargeBinary, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)  # Nueva columna

    # Relación con el modelo User
    usuario = relationship("User", back_populates="posts")
