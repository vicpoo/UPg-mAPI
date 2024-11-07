from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
# from pymongo.mongo_client import MongoClient
# from app.shared.config.mongoConnection import client
from app.shared.config.db import engine, get_db, Base
# from app.models.User import user
from fastapi.middleware.cors import CORSMiddleware
# from app.routes.userRouter import user
from app.shared.middlewares import authMiddleWare
from app.routes.userRouter import userRoutes
from app.routes.employeeRouter import employeeRoutes

app = FastAPI()

app.include_router(userRoutes)
app.include_router(employeeRoutes)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

