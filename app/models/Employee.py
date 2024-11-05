from sqlalchemy import Column, Integer, String, INT
from app.shared.config.db import Base

class employee(Base):
    __tablename__ = "empleado"

    id_empleado = Column(Integer, primary_key=True)
    id_rol = Column(Integer, nullable = True)
    nombre = Column(String, nullable= True)
    contraseña = Column(String, nullable= True)
    horario = Column(Integer, nullable=True)
    id_establecimiento = Column(Integer, nullable=True)
    id_servicio = Column(Integer, nullable=True)
