from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.schemas.admin_schema import AdminCreate, AdminResponse, AdminLogin, Token
from app.shared.config.db import get_db
from app.models.admin import Admin

# Configuración de rutas y seguridad
adminRoutes = APIRouter()
SECRET_KEY = "43d8a1f0c8b3479e9c7a5b16d3e63b93f27c8af9bfe1246a0a93c9a5d2b8450e"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

# Funciones auxiliares
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Admin).where(Admin.correo == email))
    admin = result.scalar_one_or_none()
    if admin is None:
        raise credentials_exception
    return admin

# Endpoint para crear administrador
@adminRoutes.post('/admin/', response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(admin: AdminCreate, db: AsyncSession = Depends(get_db)):
    existing_admin = await db.execute(select(Admin).where(Admin.correo == admin.correo))
    if existing_admin.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado como administrador."
        )

    hashed_password = get_password_hash(admin.contraseña)
    new_admin = Admin(
        nombre=admin.nombre,
        apellido=admin.apellido,
        correo=admin.correo,
        contraseña=hashed_password,  
        nombre_administrador=admin.nombre_administrador
    )
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return new_admin

# Endpoint para login de administrador
@adminRoutes.post("/admin/login", response_model=Token)
async def admin_login(admin: AdminLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).where(Admin.correo == admin.correo))
    db_admin = result.scalar_one_or_none()
    if not db_admin or not verify_password(admin.contraseña, db_admin.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )
    access_token = create_access_token(data={"sub": db_admin.correo})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint para obtener administrador por ID
@adminRoutes.get('/admin/{admin_id}', response_model=AdminResponse)
async def get_admin(admin_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).where(Admin.id == admin_id))
    admin = result.scalar_one_or_none()
    if admin is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado.")
    return admin

# Endpoint para actualizar administrador
@adminRoutes.put('/admin/{admin_id}', response_model=AdminResponse)
async def update_admin(
    admin_id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    correo: str = Form(...),
    contraseña: str = Form(None),
    nombre_administrador: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Admin).where(Admin.id == admin_id))
    db_admin = result.scalar_one_or_none()
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado.")

    db_admin.nombre = nombre
    db_admin.apellido = apellido
    db_admin.correo = correo
    if contraseña:
        db_admin.contraseña = get_password_hash(contraseña)
    if nombre_administrador:
        db_admin.nombre_administrador = nombre_administrador

    await db.commit()
    await db.refresh(db_admin)
    return db_admin

# Endpoint para listar todos los administradores
@adminRoutes.get('/admins/', response_model=list[AdminResponse])
async def list_admins(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin))
    admins = result.scalars().all()
    return admins

# Endpoint para eliminar administrador
@adminRoutes.delete('/admin/{admin_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(admin_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).where(Admin.id == admin_id))
    db_admin = result.scalar_one_or_none()
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado.")
    
    await db.delete(db_admin)
    await db.commit()
    return {"detail": "Administrador eliminado correctamente."}
