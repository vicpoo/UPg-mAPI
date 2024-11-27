# db.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos usando asyncpg para conexiones asíncronas
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:RutaAWS19@databasegym.cbvo0epojgpy.us-east-1.rds.amazonaws.com/databaseGYM"

# Crear el motor de la base de datos asíncrono
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Crear una sesión asíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Exponer async_session como un alias para evitar confusión
async_session = AsyncSessionLocal

# Declarar la base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
