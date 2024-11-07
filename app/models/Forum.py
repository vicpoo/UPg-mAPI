from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Enum, Text
from app.shared.config.db import Base
import enum

class GroupType(enum.Enum):
    Private = "Private"
    Public = "Public"

class Forum(Base):
    __tablename__ = "forum"
    id_forum = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    state = Column(String(255), nullable=False)
    privacy = Column(Enum(GroupType), nullable=False)
    id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False)
    password = Column(String(255), nullable=True)
    
