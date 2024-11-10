from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse, Token
from app.shared.config.db import get_db
from app.shared.middlewares.security import (
    ALGORITHM,
    SECRET_KEY,
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List  # Importación de List
import jwt

userRoutes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint de login
@userRoutes.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.correo == form_data.username).first()
    if not user or not verify_password(form_data.password, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.correo}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Registro de usuario
@userRoutes.post('/user/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.correo == user.correo).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    hashed_password = get_password_hash(user.contraseña)
    db_user = User(
        **user.dict(exclude={'contraseña'}),
        contraseña=hashed_password,
        es_premium=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Obtener información del usuario actual
@userRoutes.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(oauth2_scheme)):
    return current_user

# Obtener todos los usuarios
@userRoutes.get('/user/', response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Obtener usuario por ID
@userRoutes.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
