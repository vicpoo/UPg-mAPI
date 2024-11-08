from sqlalchemy import Column, ForeignKey, Integer
from app.shared.config.db import Base


class Chat(Base):
    __tablename__ = "chat"
    id_chat = Column(Integer, primary_key=True, autoincrement=True)
    recipient_id = Column(Integer, ForeignKey("user.id_user", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("user.id_user", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
