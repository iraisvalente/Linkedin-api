from typing import List
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware
import models,schemas
from connection import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post('/users/',response_model=schemas.User)
def create_users(entrada:schemas.User,db:Session=Depends(get_db)):
    usuario = models.User(First_Name = entrada.First_Name,Last_Name=entrada.Last_Name,Email_Address=entrada.Email_Address,Company=entrada.Company, Position=entrada.Position, Password_user=entrada.Password_user)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.post('/users/login/',response_model=schemas.User)
def login(entrada:schemas.User, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(Email_Address=entrada.Email_Address, Password_user=entrada.Password_user).first()
    db.commit()
    db.refresh(usuario)
    return usuario

@app.get('/connections/',response_model=List[schemas.Connection])
def show_connections(db:Session=Depends(get_db)):
    connections = db.query(models.Connection).all()
    return connections