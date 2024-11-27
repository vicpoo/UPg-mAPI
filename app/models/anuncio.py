from sqlalchemy import Column, Integer, LargeBinary
from app.shared.config.db import Base

class Anuncio(Base):
    __tablename__ = "anuncios"

    id = Column(Integer, primary_key=True, index=True)
    imagen = Column(LargeBinary, nullable=True)  # Imagen en formato bytea