from pydantic import BaseModel
import base64
from typing import Optional

class CommentBase(BaseModel):
    contenido: str

class CommentCreate(CommentBase):
    publicacion_id: int
    usuario_id: int


class CommentResponse(BaseModel):
    id: int
    contenido: str
    publicacion_id: int
    usuario_nombre: Optional[str]  # Nombre del usuario que hizo el comentario
    usuario_foto: Optional[str]  # Foto de perfil en Base64 del usuario que hizo el comentario

    class Config:
        orm_mode = True

    @staticmethod
    def encode_image(image_data: Optional[bytes]) -> Optional[str]:
        """Convierte los datos binarios de la imagen a una cadena en base64"""
        if image_data:
            return base64.b64encode(image_data).decode('utf-8')
        return None

