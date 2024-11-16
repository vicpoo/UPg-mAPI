from typing import List
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse, Token, UserLogin
from app.shared.config.db import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

userRoutes = APIRouter()

# JWT configuration and security settings
SECRET_KEY = "3b29f8d55cb94482a2e459cb5d7e9b3e68de5463bce117ef7c8d3c1c2b6b12a8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
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

# Endpoint to create a new user (no authentication required)
@userRoutes.post('/user/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if the email is already registered
    result = await db.execute(select(User).where(User.correo == user.correo))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    hashed_password = get_password_hash(user.contraseña)
    db_user = User(
        nombre_usuario=user.nombre_usuario,
        correo=user.correo,
        contraseña=hashed_password,
        descripcion=user.descripcion,
        es_premium=user.es_premium
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Endpoint to log in and generate a token (no authentication required)
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

# Endpoint to get all users (authentication required)
@userRoutes.get('/users/', response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

# Endpoint to get the current user's profile (authentication required)
@userRoutes.get('/user/me', response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint to update a user by ID (authentication required)
@userRoutes.put('/user/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value if key != "contraseña" else get_password_hash(value))
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Endpoint to delete a user by ID (authentication required)
@userRoutes.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted"}
