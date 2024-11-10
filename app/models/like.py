from sqlalchemy import Column, Integer, ForeignKey
from app.shared.config.db import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    publicacion_id = Column(Integer, ForeignKey("publicacion.id"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
