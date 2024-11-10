from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Text
from app.shared.config.db import Base

class User(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contraseña = Column(String, nullable=False)
    foto_perfil = Column(LargeBinary, nullable=True)
    descripcion = Column(Text, nullable=True)
    es_premium = Column(Boolean, default=False)
