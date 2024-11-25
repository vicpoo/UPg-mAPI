from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Text
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class User(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)
    foto_perfil = Column(LargeBinary, nullable=True)  # Almacena binarios
    descripcion = Column(Text, nullable=True)
    es_premium = Column(Boolean, default=False)

    # Relación con el modelo Respuesta
    respuestas = relationship("Respuesta", back_populates="usuario")
    questions = relationship("Question", back_populates="usuario")
    # Relación con otros modelos
    posts = relationship("Post", back_populates="usuario")
    comentarios = relationship("Comment", back_populates="usuario")
    porcentajes_grasa = relationship("PorcentajeGrasa", back_populates="usuario", lazy='select')