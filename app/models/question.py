from sqlalchemy import Column, Integer, Text, ForeignKey
from app.shared.config.db import Base

class Question(Base):
    __tablename__ = "pregunta"

    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
