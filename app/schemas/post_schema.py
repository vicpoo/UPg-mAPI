from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime
    forum_id: int

    model_config = ConfigDict(from_attributes=True)
    
class PostCreate(PostBase):
    publication_date: datetime | None = None

class PostResponse(PostBase):
    id_post: int
    publication_date: datetime
    user_id: int

