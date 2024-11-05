from pydantic import BaseModel; 


class EmployeeBase(BaseModel):
    id_empleado: int
    id_rol: int
    nombre: str
    contraseña: str
    horario: int
    id_establecimiento: int
    id_servicio: int

    class config:
        orm_mode = True
class EmployeeRequest(EmployeeBase):
    class config:
        orm_mode = True

class EmployeeResponse(EmployeeBase):
    id: int

    class config:
        orm_mode = True