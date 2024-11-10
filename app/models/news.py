from sqlalchemy import Column, Integer, String, Text
from app.shared.config.db import Base

class News(Base):
    __tablename__ = "noticia"

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    resumen = Column(Text, nullable=True)
    contenido_completo = Column(Text, nullable=False)
