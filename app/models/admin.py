from sqlalchemy import Column, Integer, String, ForeignKey
from app.shared.config.db import Base

class Admin(Base):
    __tablename__ = "administrador"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)  # Asegura que el correo sea único
    contraseña = Column(String, nullable=False)  # Cifrar contraseñas es importante
    nombre_administrador = Column(String, nullable=False)  # Campo adicional si es requerido
