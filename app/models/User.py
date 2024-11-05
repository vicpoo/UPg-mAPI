from sqlalchemy import Column, Integer, String, INT
from app.shared.config.db import Base

class user(Base):
    __tablename__ = "rol"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True); 

