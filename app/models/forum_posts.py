from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Enum, Text
from app.shared.config.db import Base
import enum

class GroupType(enum.Enum):
    Private = "Private"
    Public = "Public"

class ForumPosts(Base):
    __tablename__ = "forum_posts"
    id_post = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    publication_date = Column(DateTime, nullable=False)
    forum_id = Column(Integer, ForeignKey("forum.id_forum", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id_user", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
