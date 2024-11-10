from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost:5433/upgym")




# Crear el motor de la base de datos asíncrona
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Crear una sesión asíncrona
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Declarar la base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
async def get_db():
    async with SessionLocal() as session:
        yield session
