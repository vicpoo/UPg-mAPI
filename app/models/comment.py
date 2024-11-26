from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class Comment(Base):
    __tablename__ = "comentario"

    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    publicacion_id = Column(Integer, ForeignKey("publicacion.id", ondelete="CASCADE"))  # Cascada en la base de datos
    usuario_id = Column(Integer, ForeignKey("usuario.id"))



    # Relación con el modelo User
    usuario = relationship("User", back_populates="comentarios")
    publicacion = relationship("Post", back_populates="comentarios")