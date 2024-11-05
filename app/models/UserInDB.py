from pydantic import BaseModel
from app.models.Employee import employee

class UserInDB(employee):
    hashed_password: str
    