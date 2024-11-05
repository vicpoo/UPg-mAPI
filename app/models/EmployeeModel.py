from pydantic import BaseModel; 

class EmployeeResponse(BaseModel):
    id_empleado: int
    id_rol: int
    nombre: str
    contraseña: str
    horario: int
    id_establecimiento: int
    id_servicio: int
    
    class config():
        orm_mode = True