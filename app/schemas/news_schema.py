from pydantic import BaseModel

class NewsBase(BaseModel):
    titulo: str
    resumen: str | None = None
    contenido_completo: str
    imagen: str | None = None  # La imagen se manejará como Base64 en las respuestas

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int
