from sqlalchemy import Column, Integer, String, ForeignKey
from app.shared.config.db import Base

class Admin(Base):
    __tablename__ = "administrador"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
