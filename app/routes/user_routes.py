from fastapi import APIRouter, Query, Depends, HTTPException, status, File, UploadFile, Form
from typing import List
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user_schema import UserCreate, UserResponse, Token, UserLogin
from app.shared.config.db import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import base64
from app.models.User import User

userRoutes = APIRouter()

SECRET_KEY = "3b29f8d55cb94482a2e459cb5d7e9b3e68de5463bce117ef7c8d3c1c2b6b12a8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.correo == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


# Create a new user
@userRoutes.post('/user/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.correo == user.correo))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    hashed_password = get_password_hash(user.contraseña)
    new_user = User(
        nombre_usuario=user.nombre_usuario,
        correo=user.correo,
        contraseña=hashed_password,
        descripcion=user.descripcion,
        es_premium=user.es_premium,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# Get current user profile
@userRoutes.get('/user/me', response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    if current_user.foto_perfil:
        current_user.foto_perfil = base64.b64encode(current_user.foto_perfil).decode('utf-8')
    return current_user


# Update user details
@userRoutes.put('/user/{user_id}', response_model=UserResponse)
async def update_user(
    user_id: int,
    nombre_usuario: str = Form(...),
    descripcion: str = Form(...),
    foto_perfil: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.nombre_usuario = nombre_usuario
    db_user.descripcion = descripcion
    if foto_perfil:
        db_user.foto_perfil = await foto_perfil.read()

    await db.commit()
    await db.refresh(db_user)

    if db_user.foto_perfil:
        db_user.foto_perfil = base64.b64encode(db_user.foto_perfil).decode('utf-8')

    return db_user


# User login
@userRoutes.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.nombre_usuario == user.nombre_usuario))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.contraseña, db_user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )
    access_token = create_access_token(data={"sub": db_user.correo})
    return {"access_token": access_token, "token_type": "bearer"}


# Search users by username
@userRoutes.get("/search", response_model=List[UserResponse])
async def search_users(
    query: str = Query(..., min_length=1, description="Texto a buscar en el nombre de usuario"),
    limit: int = Query(5, ge=1, le=50, description="Número máximo de resultados a devolver"),
    db: AsyncSession = Depends(get_db)
):
    results = await db.execute(
        select(User)
        .where(User.nombre_usuario.ilike(f"{query}%"))
        .limit(limit)
    )
    users = results.scalars().all()

    for user in users:
        if user.foto_perfil:
            user.foto_perfil = base64.b64encode(user.foto_perfil).decode('utf-8')

    return users


# Get all users
@userRoutes.get('/users', response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()

    for user in users:
        if user.foto_perfil:
            user.foto_perfil = base64.b64encode(user.foto_perfil).decode('utf-8')

    return users


from base64 import b64encode

@userRoutes.patch('/user/{user_id}/premium', response_model=UserResponse)
async def update_es_premium(
    user_id: int,
    es_premium: bool = Form(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.es_premium = es_premium
    await db.commit()
    await db.refresh(db_user)

    # Codificar `foto_perfil` en Base64 si existe
    if db_user.foto_perfil:
        db_user.foto_perfil = b64encode(db_user.foto_perfil).decode('utf-8')

    return db_user
