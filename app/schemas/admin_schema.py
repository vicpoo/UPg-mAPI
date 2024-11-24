from pydantic import BaseModel, EmailStr
from typing import Optional

class AdminBase(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    nombre_administrador: Optional[str] = None

class AdminCreate(AdminBase):
    contraseña: str  

class AdminResponse(AdminBase):
    id: int

    class Config:
        orm_mode = True

class AdminLogin(BaseModel):
    correo: EmailStr
    contraseña: str  

class Token(BaseModel):
    access_token: str
    token_type: str
