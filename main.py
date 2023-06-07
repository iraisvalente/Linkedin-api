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

@app.get('/connections/firstname/{firstname}',response_model=List[schemas.Connection])
def show_connections_by_firstname(firstname: str, db:Session=Depends(get_db)):
    connections = db.query(models.Connection).filter_by(First_Name=firstname).all()
    return connections

@app.get('/connections/lastname/{lastname}',response_model=List[schemas.Connection])
def show_connections_by_lastname(lastname: str, db:Session=Depends(get_db)):
    connections = db.query(models.Connection).filter_by(Last_Name=lastname).all()
    return connections

@app.get('/connections/email/{email}',response_model=List[schemas.Connection])
def show_connections_by_email(email: str, db:Session=Depends(get_db)):
    connections = db.query(models.Connection).filter_by(Email_Address=email).all()
    return connections

@app.get('/connections/company/{company}',response_model=List[schemas.Connection])
def show_connections_by_company(company: str, db:Session=Depends(get_db)):
    connections = db.query(models.Connection).filter_by(Company=company).all()
    return connections

@app.get('/connections/position/{position}',response_model=List[schemas.Connection])
def show_connections_by_(position: str, db:Session=Depends(get_db)):
    connections = db.query(models.Connection).filter_by(Position=position).all()
    return connections

@app.get('/connections/connection/{connection}',response_model=List[schemas.Connection])
def show_connections_by_(connection: str, db:Session=Depends(get_db)):
    connections = db.query(models.Connection).filter_by(Connection=connection).all()
    return connections

@app.post('/connections/',response_model=List[schemas.Connection])
def show_connections_all_filters(entrada:schemas.Connection, db:Session=Depends(get_db)):
    connections = db.query(models.Connection).filter_by(First_Name=entrada.First_Name, Last_Name=entrada.Last_Name, Email_Address=entrada.Email_Address, Company=entrada.Company, Position=entrada.Position, Connection=entrada.Connection).all()
    return connections

@app.get('/common_positions/',response_model=List[schemas.Position])
def common_positions(db:Session=Depends(get_db)):
    positions = db.execute('''
        SELECT Position, COUNT(*) as Count 
        FROM Connections 
        GROUP BY Position 
        ORDER BY COUNT(Position) 
        DESC LIMIT 5
    ''')
    return positions.all()

@app.get('/common_companies/',response_model=List[schemas.Company])
def common_companies(db:Session=Depends(get_db)):
    companies = db.execute('''
        SELECT Company, COUNT(*) as Count 
        FROM Connections 
        GROUP BY Company 
        ORDER BY COUNT(Company)
        DESC LIMIT 5
    ''')
    return companies.all()

@app.get('/common_connections/',response_model=List[schemas.CommonConnection])
def common_companies(db:Session=Depends(get_db)):
    connections = db.execute('''
        SELECT Connection, COUNT(*) as Count 
        FROM Connections 
        GROUP BY Connection 
        ORDER BY COUNT(Connection)
        DESC LIMIT  5
    ''')
    return connections.all()

@app.get('/company_positions/{company}',response_model=List[schemas.Position])
def common_companies(company: str, db:Session=Depends(get_db)):
    positions = db.execute('''
        SELECT Position, COUNT(*) AS Count
        FROM Connections where Company = '''+company+''' GROUP BY Position;
    ''')
    return positions.all()

@app.get('/all_companies/',response_model=List[schemas.Company])
def all_companies(db:Session=Depends(get_db)):
    companies = db.execute('''
        SELECT Company 
        FROM Connections
    ''')
    return companies.all()

@app.get('/all_positions/',response_model=List[schemas.Position])
def all_positions(db:Session=Depends(get_db)):
    positions = db.execute('''
        SELECT Position 
        FROM Connections
    ''')
    return positions.all()