from pydantic import BaseModel

class MuscleGroupBase(BaseModel):
    nombre: str
    imagen: bytes | None = None

class MuscleGroupCreate(MuscleGroupBase):
    pass

class MuscleGroupResponse(MuscleGroupBase):
    id: int
