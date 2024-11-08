from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from app.shared.config.db import Base

class UserForum(Base):
    __tablename__ = "user_forum"
    id_member = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id_user", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    id_forum = Column(Integer, ForeignKey("forum.id_forum", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    join_date = Column(DateTime, nullable=False)

