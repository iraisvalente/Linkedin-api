from typing import List
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware
import models,schemas
from connection import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

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
    positions = db.execute(text("SELECT Position, COUNT(*) as Count FROM Connections GROUP BY Position ORDER BY COUNT(Position) DESC LIMIT 5"))
    return positions.all()

@app.get('/common_companies/',response_model=List[schemas.Company])
def common_companies(db:Session=Depends(get_db)):
    companies = db.execute(text("SELECT Company, COUNT(*) as Count FROM Connections GROUP BY Company ORDER BY COUNT(Company) DESC LIMIT 5"))
    return companies.all()

@app.get('/common_connections/',response_model=List[schemas.CommonConnection])
def common_companies(db:Session=Depends(get_db)):
    connections = db.execute(text("SELECT Connection,COUNT(*) as Count FROM Connections GROUP BY Connection ORDER BY COUNT(Connection) DESC LIMIT 5"))
    return connections.all()

@app.get('/company_positions/{company}',response_model=List[schemas.Position])
def individual_company_positions(company: str, db:Session=Depends(get_db)):
    positions = db.execute(text('''SELECT Position, COUNT(*) AS Count FROM Connections where Company LIKE '''+company+''' GROUP BY Position'''))
    return positions.all()

@app.get('/all_companies/',response_model=List[schemas.Company])
def all_companies(db:Session=Depends(get_db)):
    companies = db.execute(text('''
        SELECT DISTINCT Company 
        FROM Connections
    '''))
    return companies.all()

@app.get('/all_positions/',response_model=List[schemas.Position])
def all_positions(db: Session = Depends(get_db)):
    positions = db.execute(text('''
        SELECT DISTINCT Position
        FROM Connections
        ORDER BY Position ASC
    ''')).all()
    return positions

@app.get('/user_connections/{connection}',response_model=List[schemas.Connection])
def user_connections(connection: str, db:Session=Depends(get_db)):
    print(connection)
    connections = db.execute(text('''
        SELECT First_Name, Last_Name, Email_Address, Company, Position FROM Connections WHERE Connection LIKE "%'''+connection+'''%"                  
    ''')).all()  
    
    return connections

@app.get('/connections/{company}',response_model=List[schemas.Connection])
def company_positions(company: str, db:Session=Depends(get_db)):
    connections = db.execute(text('''
        SELECT * FROM Connections 
        WHERE Company LIKE '''+company+'''                  
    ''')).all()  
    
    return connections

@app.get('/company_positions/')
def company_positions(db:Session=Depends(get_db)):
    results = db.execute(text('''
            SELECT Company, 
            Position, COUNT(*) AS Position_Count 
            FROM Connections 
            GROUP BY Company, Position 
            ORDER BY Company ASC
        ''')).all()

    companies = []
    current_company = None
    for row in results:
        if row[0] != current_company:        
            current_company = row[0]
            company = {
                "Company": current_company,
                "Positions": []
            }
            if current_company:
                companies.append(company)

        position = {
            "Position": row[1],
            "Count": str(row[2])
        }
        company["Positions"].append(position)

    if current_company:
        companies.append(company)
    
    companies.pop()

    return companies


@app.get('/unique_names/',response_model=schemas.Count)
def unique_names(db: Session = Depends(get_db)):
    query = text('SELECT COUNT(DISTINCT First_Name) as count FROM Connections')
    result = db.execute(query)
    count = result.scalar()
    return {'Count': count}

@app.get('/unique_companies/',response_model=schemas.Count)
def unique_companies(db: Session = Depends(get_db)):
    query = text('SELECT COUNT(DISTINCT Company) FROM Connections')
    result = db.execute(query)
    count = result.scalar()
    return {'Count': count}

@app.get('/unique_positions/',response_model=schemas.Count)
def unique_positions(db: Session = Depends(get_db)):
    query = text('SELECT COUNT(DISTINCT Position) FROM Connections;')
    result = db.execute(query)
    count = result.scalar()
    return {'Count': count}

@app.get('/last_connections_added/', response_model=List[schemas.Connection])
def last_connections_added(db: Session = Depends(get_db)):
    query = text('''
            SELECT *
            FROM Connections
            WHERE Upload_Date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        ''')
    result = db.execute(query).all()
    return result

@app.post('/connection_independent_search/', response_model=List[schemas.Connection])
def connection_independent_search(connection: schemas.Connection, db: Session = Depends(get_db)):
    query = text('''
        SELECT * FROM Connections 
        WHERE (First_Name = :first_name OR First_Name LIKE :first_name) 
        OR (Last_Name = :last_name OR Last_Name LIKE :last_name) 
        OR (Email_Address = :email_address OR Last_Name LIKE :email_address) 
        OR (Company = :company OR Company LIKE :company) 
        OR (Position = :position OR Position LIKE :position) 
        OR (Connection = :connection OR Connection LIKE :connection) 
    ''')

    parameters = {
        'first_name': connection.First_Name if connection.First_Name != "" else "",
        'last_name': connection.Last_Name if connection.Last_Name != "" else "",
        'email_address': connection.Email_Address if connection.Email_Address != "" else "",
        'company': connection.Company if connection.Company != "" else "",
        'position': connection.Position if connection.Position != "" else "",
        'connection': connection.Connection if connection.Connection != "" else "",
    }

    result = db.execute(query, parameters).all()
    return result

@app.post('/connection_dependent_search/', response_model=List[schemas.Connection])
def connection_dependent_search(connection: schemas.Connection, db: Session = Depends(get_db)):
    query = text('''
        SELECT * FROM Connections 
        WHERE First_Name LIKE :first_name
        AND Last_Name LIKE :last_name
        AND Email_Address LIKE :email_address
        AND Company LIKE :company
        AND Position LIKE :position
        AND Connection LIKE :connection
    ''')

    parameters = {
        'first_name': f"%{connection.First_Name}%",
        'last_name': f"%{connection.Last_Name}%",
        'email_address': f"%{connection.Email_Address}%",
        'company': f"%{connection.Company}%",
        'position': f"%{connection.Position}%",
        'connection': f"%{connection.Connection}%",
    }
    
    result = db.execute(query, parameters).all()
    return result