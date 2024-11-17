from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    descripcion: Optional[str] = None
    es_premium: bool = False

class UserCreate(UserBase):
    contraseña: str

class UserLogin(BaseModel):
    nombre_usuario: str
    contraseña: str

class UserUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    descripcion: Optional[str] = None
    foto_perfil: Optional[bytes] = None

class UserResponse(UserBase):
    id: int
    foto_perfil: Optional[str] = None

    class Config:
        from_attributes = True
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    correo: Optional[str] = None
