from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    descripcion: str | None = None
    es_premium: bool = False

class UserCreate(UserBase):
    contraseña: str

class UserResponse(UserBase):
    id: int
    foto_perfil: bytes | None = None

# Esquema para el token
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema opcional para almacenar información en el token
class TokenData(BaseModel):
    correo: str | None = None
