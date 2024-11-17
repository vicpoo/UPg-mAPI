from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)
    foto_perfil = Column(LargeBinary, nullable=True)
    descripcion = Column(Text, nullable=True)
    es_premium = Column(Boolean, default=False)
