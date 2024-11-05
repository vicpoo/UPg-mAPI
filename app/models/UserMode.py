from pydantic import BaseModel; 

class userResponse(BaseModel):
    id: int
    name: str

class config:
    orm_mode = True