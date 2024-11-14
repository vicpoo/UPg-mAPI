from pydantic import BaseModel
from enum import Enum
from typing import Optional

class Nivel(str, Enum):
    BASICO = "BASICO"
    INTERMEDIO = "INTERMEDIO"
    AVANZADO = "AVANZADO"

class UbicacionEjercicio(str, Enum):
    CASA = "CASA"
    GYM = "GYM"

class ExerciseBase(BaseModel):
    titulo: str
    resumen: Optional[str] = None
    nivel: Nivel
    tiempo_descanso: Optional[int] = None
    repeticiones: Optional[int] = None
    imagen: Optional[bytes] = None
    ubicacion: UbicacionEjercicio

class ExerciseCreate(ExerciseBase):
    grupo_muscular_id: Optional[int] = None

class ExerciseResponse(ExerciseBase):
    id: int
    grupo_muscular_id: Optional[int] = None
