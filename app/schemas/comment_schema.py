from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentBase(BaseModel):
    comment_text: str
    comment_date: datetime
    post_id: int

    model_config = ConfigDict(from_attributes=True)
    
class CommentCreate(CommentBase):
    comment_date: datetime | None = None

class CommentResponse(CommentBase):
    id_comment: int
    comment_date: datetime
    user_id: int
