from pydantic import BaseModel
from typing import Optional

class NivelEjercicioBase(BaseModel):
    nivel: str

class NivelEjercicioCreate(NivelEjercicioBase):
    pass

class NivelEjercicioUpdate(BaseModel):
    nivel: Optional[str] = None

class NivelEjercicioResponse(NivelEjercicioBase):
    id: int

    class Config:
        orm_mode = True
