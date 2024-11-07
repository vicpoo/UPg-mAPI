from sqlalchemy import Column, DateTime, Integer, String, Boolean
from app.shared.config.db import Base

class User(Base):
    __tablename__ = "user"
    id_user = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    mail = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(String(255), nullable=False)
    rol = Column(String(255), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    state = Column(String(255), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)