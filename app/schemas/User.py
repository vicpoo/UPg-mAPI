from pydantic import BaseModel; 


class UserBase(BaseModel):
    id: int
    name: str

    class config:
        orm_mode = True

class userRequest(UserBase):
    class config:
        orm_mode = True

class userResponse(UserBase):
    id: int


    class config:
        orm_mode = True