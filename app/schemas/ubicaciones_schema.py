from pydantic import BaseModel
from typing import Optional

class UbicacionBase(BaseModel):
    ubicacion: str

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionUpdate(BaseModel):
    ubicacion: Optional[str] = None

class UbicacionResponse(UbicacionBase):
    id: int

    class Config:
        orm_mode = True
