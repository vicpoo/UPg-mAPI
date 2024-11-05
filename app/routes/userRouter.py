from fastapi import APIRouter; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
import app.models
from app.models.User import user
from app.schemas.User import userRequest, userResponse
from app.models.UserMode import userResponse


Base.metadata.create_all(bind=engine)
rolRoutes = APIRouter() 


@rolRoutes.post('/users/', status_code=status.HTTP_201_CREATED, response_model=userResponse)
async def create_user(post_user: userRequest, db: Session = Depends(get_db)):
    new_user = user(**post_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.__dict__



@rolRoutes.get('/users/', status_code= status.HTTP_200_OK, response_model= List[userResponse])
async def get_roles(db: Session = Depends(get_db)):
    all_roles = db.query(user).all(); 
    for i in all_roles:
        print("rol" + i.name)
    return all_roles; 

@rolRoutes.put("/users/${id_rol}", response_model=userResponse)
async def change_rol(id_rol: int, userChange: userRequest,db: Session = Depends(get_db)): 
    change_rol = db.query(user).filter(user.id == id_rol).first()
    if change_rol is None:

        raise HTTPException(
            status_code=404,
            detail="rol no encontrado"
        )
    
    for key, value in userChange.dict().items():
        setattr(
            change_rol, 
            key, value
        )
    
    db.commit()
    db.refresh(change_rol)
    return change_rol

@rolRoutes.delete("/users/${id_rol}", response_model=userResponse)
async def delete_rol(id_rol: int, db: Session = Depends(get_db)):
    delete_rol = db.query(user).filter(user.id == id_rol).first()
    if delete_rol is None:
    
        raise HTTPException(
            status_code=404, 
            detail="rol no encontrado"
        )
    
    db.delete(delete_rol)
    db.commit()
    return delete_rol
    