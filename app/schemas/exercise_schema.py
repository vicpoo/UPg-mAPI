from pydantic import BaseModel
from enum import Enum

class Nivel(str, Enum):
    BASICO = "BASICO"
    INTERMEDIO = "INTERMEDIO"
    AVANZADO = "AVANZADO"

class UbicacionEjercicio(str, Enum):
    CASA = "CASA"
    GYM = "GYM"

class ExerciseBase(BaseModel):
    titulo: str
    resumen: str | None = None
    nivel: Nivel
    tiempo_descanso: int | None = None
    repeticiones: int | None = None
    imagen: bytes | None = None
    ubicacion: UbicacionEjercicio

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    id: int
    grupo_muscular_id: int
