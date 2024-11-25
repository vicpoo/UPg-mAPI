import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.shared.config.db import engine, Base

# Importar las rutas creadas
from app.routes.user_routes import userRoutes
from app.routes.post_routes import postRoutes
from app.routes.comment_routes import commentRoutes
from app.routes.news_routes import newsRoutes
from app.routes.question_routes import questionRoutes
from app.routes.like_routes import likeRoutes
from app.routes.muscle_group_routes import muscleGroupRoutes
from app.routes.exercise_routes import exerciseRoutes
from app.routes.respuesta_routes import respuestaRoutes
from app.routes.admin_routes import adminRoutes
from app.routes.PorcentajeGrasa_routes import porcentajeGrasaRoutes


# Inicializar la aplicación FastAPI
app = FastAPI()

# Incluir las rutas creadas
app.include_router(userRoutes)
app.include_router(postRoutes)
app.include_router(commentRoutes)
app.include_router(newsRoutes)
app.include_router(questionRoutes)
app.include_router(likeRoutes)
app.include_router(muscleGroupRoutes)
app.include_router(exerciseRoutes)
app.include_router(respuestaRoutes)
app.include_router(adminRoutes)
app.include_router(porcentajeGrasaRoutes)

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],    # Métodos permitidos
    allow_headers=["*"],    # Encabezados permitidos
)



# Función asíncrona para crear todas las tablas en la base de datos
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Ejecutar la creación de tablas cuando se inicia la aplicación
@app.on_event("startup")
async def startup():
    await create_tables()

# Ruta raíz para verificar el estado de la API
@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de UPgym"}
