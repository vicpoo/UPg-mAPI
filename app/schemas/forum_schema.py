from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ForumBase(BaseModel):
    name: str
    description: str
    creation_date: datetime
    state: str
    privacy: str
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)
    
class ForumCreate(ForumBase):
    creation_date: datetime | None = None

class ForumResponse(ForumBase):
    id_forum: int
    creation_date: datetime
    id_user: int
