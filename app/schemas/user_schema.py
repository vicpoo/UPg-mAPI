from pydantic import BaseModel, EmailStr
from typing import Optional

# Base model para usuario
class UserBase(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    descripcion: Optional[str] = None
    es_premium: bool = False

# Modelo para crear un usuario
class UserCreate(UserBase):
    contraseña: str

# Modelo para login de usuario
class UserLogin(BaseModel):
    nombre_usuario: str
    contraseña: str

# Modelo para actualizar un usuario
class UserUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    descripcion: Optional[str] = None
    foto_perfil: Optional[bytes] = None

# Modelo para la respuesta del usuario
class UserResponse(UserBase):
    id: int
    foto_perfil: Optional[str] = None  # Convertiremos a Base64 en la ruta si es necesario

    class Config:
        from_attributes = True  # Esta línea corrige el problema de Pydantic v2

# Modelo para el token de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

# Modelo para datos de token
class TokenData(BaseModel):
    correo: Optional[str] = None
