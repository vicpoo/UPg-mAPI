from sqlalchemy import Column, Integer, Text, ForeignKey
from app.shared.config.db import Base

class Comment(Base):
    __tablename__ = "comentario"

    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    publicacion_id = Column(Integer, ForeignKey("publicacion.id"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
