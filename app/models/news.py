from sqlalchemy import Column, Integer, String, Text, LargeBinary
from app.shared.config.db import Base

class News(Base):
    __tablename__ = "noticia"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    resumen = Column(Text, nullable=True)
    contenido_completo = Column(Text, nullable=False)
    imagen = Column(LargeBinary, nullable=True)  # Almacena la imagen como binario
