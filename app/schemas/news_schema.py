from pydantic import BaseModel

class NewsBase(BaseModel):
    titulo: str
    resumen: str | None = None
    contenido_completo: str

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int
