from pydantic import BaseModel

class PorcentajeGrasaCreate(BaseModel):
    genero: str
    altura: float
    cintura: float
    resultado: float  # Aseguramos que el resultado ya esté calculado y se pase desde el frontend

    class Config:
        # Aseguramos que el modelo esté alineado con los tipos de la base de datos
        orm_mode = True

class PorcentajeGrasaResponse(PorcentajeGrasaCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

    @classmethod
    def from_create(cls, data: PorcentajeGrasaCreate, user_id: int) -> "PorcentajeGrasaResponse":
        return cls(id=0,  # Asigna el ID adecuado cuando se cree
                   user_id=user_id, 
                   **data.dict())
