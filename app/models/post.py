from sqlalchemy import Column, Integer, Text, LargeBinary, ForeignKey
from app.shared.config.db import Base

class Post(Base):
    __tablename__ = "publicacion"

    id = Column(Integer, primary_key=True)
    descripcion = Column(Text, nullable=False)
    imagen = Column(LargeBinary, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
