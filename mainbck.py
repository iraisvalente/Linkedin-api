from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware
import models, schemas
from connection import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from scripts.bard import bard
from scripts.newsearch import make_search
from scripts.linked import choice, download, extract, append, append_copy
from datetime import datetime
import os
import pathlib
import shutil
from datetime import datetime
import subprocess
from time import sleep





from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome  import ChromeDriverManager
from selenium.webdriver import ActionChains




options = Options()
options.add_argument("start-maximized"); 
#options.add_argument("--headless"); 
options.add_argument("disable-infobars"); 
options.add_argument("--disable-extensions"); 
options.add_argument("--disable-gpu"); 
options.add_argument("--disable-dev-shm-usage"); 
options.add_argument("--no-sandbox");
options.add_experimental_option('excludeSwitches', ['enable-logging'])



login=0
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get("https://accounts.google.com/")
sleep(10)
search_bar = driver.find_element(By.ID,"identifierId")
search_bar.clear()
search_bar.send_keys(f"Aiver1@aiver.ai{Keys.RETURN}")
sleep(10)
search_bar = driver.find_element(By.NAME,"Passwd")
search_bar.clear()
search_bar.send_keys(f"Aiver!2023!{Keys.RETURN}")
sleep(10)
driver.get("https://www.linkedin.com/login")
sleep(10)
search_bar = driver.find_element(By.ID,"username")
search_bar.clear()
search_bar.send_keys("Aiver1@aiver.ai")
search_bar = driver.find_element(By.ID,"password")
search_bar.clear()
search_bar.send_keys(f"Aiver!2023!{Keys.RETURN}")
sleep(15)
login=1





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

@app.get('/common_positions/',response_model=List[schemas.PositionCount])
def common_positions(db:Session=Depends(get_db)):
    positions = db.execute(text(
        '''
            SELECT Position, COUNT(*) AS Count
            FROM Connections
            WHERE Position <> 'NaN'
            GROUP BY Position
            ORDER BY Count DESC
            LIMIT 5;
        '''))
    return positions.all()

@app.get('/common_companies/',response_model=List[schemas.CompanyCount])
def common_companies(db:Session=Depends(get_db)):
    companies = db.execute(text(
        '''
            SELECT Company, COUNT(*) as Count 
            FROM Connections 
            WHERE Company <> 'NaN'
            GROUP BY Company 
            ORDER BY COUNT(Company) 
            DESC LIMIT 5;
        '''))
    return companies.all()

@app.get('/common_connections/',response_model=List[schemas.CommonConnection])
def common_companies(db:Session=Depends(get_db)):
    connections = db.execute(text(
        '''
        SELECT Connection, COUNT(*) as Count 
        FROM Connections 
        WHERE Connection <> 'NaN'
        GROUP BY Connection 
    connections = db.query(models.Connection).filter_by(Email_Address=email).all()
        ORDER BY COUNT(Connection) 
        DESC LIMIT 5
        '''))
    return connections.all()

@app.get('/company_positions/{company}',response_model=List[schemas.PositionCount])
def individual_company_positions(company: str, db:Session=Depends(get_db)):
    positions = db.execute(text('''SELECT Position, COUNT(*) AS Count FROM Connections where Company LIKE '''+company+''' GROUP BY Position'''))
    return positions.all()

@app.get('/all_companies/',response_model=List[schemas.CompanyCount])
def all_companies(db:Session=Depends(get_db)):
    companies = db.execute(text('''
        SELECT DISTINCT Company 
        FROM Connections
    '''))
    return companies.all()

@app.get('/all_positions/',response_model=List[schemas.PositionCount])
def all_positions(db: Session = Depends(get_db)):
    positions = db.execute(text('''
        SELECT DISTINCT Position
        FROM Connections
        ORDER BY Position ASC
    ''')).all()
    return positions

@app.get('/user_connections/{connection}',response_model=List[schemas.Connection])
def user_connections(connection: str, db:Session=Depends(get_db)):
    connections = db.execute(text('''
        SELECT First_Name, Last_Name, Email_Address, Company, Position FROM Connections WHERE Connection LIKE "%'''+connection+'''%"                  
    ''')).all()  
    
    return connections

@app.get('/connections/{company}',response_model=List[schemas.Connection])
def company_positions(company: str, db:Session=Depends(get_db)):
    connections = db.execute(text('''
        SELECT * FROM Connections 
        WHERE Company LIKE "'''+company+'''"                  
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

@app.post('/connections/bard_connection/', response_model=schemas.Connection)
def bard_connection(connection: schemas.Connection, db:Session=Depends(get_db)):
    positions = db.execute(text(
        '''SELECT * FROM Connections 
            WHERE First_Name LIKE "%'''+connection.First_Name+'''%" 
            AND Last_Name LIKE "%'''+connection.Last_Name+'%"')).first()
    if positions is None:
        return {}
    return positions

@app.post('/bard/ask/')
def bard_ask(ask: schemas.Bard):
    if len(ask.company)==0 or len(ask.position)==0:
        return {"answer": "Need company and position"}
    return bard(ask.company, ask.position)

@app.post('/linked/choice/')
def linked_choice(linked: schemas.Linked):
    if len(linked.username)==0 or len(linked.password)==0:
        return {"result": "User or password not defined"}
    return choice(linked.username, linked.password)

@app.post('/linked/download/')
def linked_download(linked: schemas.Linked):
    if len(linked.username)==0 or len(linked.password)==0:
        return {"result": "User or password not defined"}
    return download(linked.username, linked.password)

@app.get('/linked/extract/')
def linked_extract():
    return extract()

@app.post('/linked/append/')
def linked_append(linked: schemas.Linked):
    if len(linked.username)==0:
        return {"result": "You need to send the mail connection"}
    return append(linked.username)

@app.post("/linked/copy/{email}")
async def linked_copy(email: str, file: UploadFile = File(...)):
    contents = file.file  
    
    try:
        ROOT_DIR = pathlib.Path().resolve()
        unzip_path = os.path.join(ROOT_DIR, "LinkedIn", "unzip")
        now = datetime.now()
        name_format = now.strftime("%m-%d-%Y")
        folder_name = f"Basic_LinkedInDataExport_{name_format}"
        
        if not os.path.exists(os.path.join(unzip_path, folder_name)):
            new_folder_name = folder_name
        else:
            version = 1
            while os.path.exists(os.path.join(unzip_path, f"{folder_name} ({version})")):
                version += 1
            new_folder_name = f"{folder_name} ({version})"
            
        os.makedirs(os.path.join(unzip_path, new_folder_name))
        file_path = os.path.join(unzip_path, new_folder_name, file.filename)
            
        with open(file_path, "wb") as f:
            shutil.copyfileobj(contents, f)
            
        result_append = append(email)
        print(result_append)
        return {"result": "Copied"}
    except Exception as e:
        return {"result": str(e)}

@app.get('/search/position/', response_model=List[schemas.Position])
def get_all_positions(db: Session = Depends(get_db)):
    positions = db.query(models.Position).all()
    return positions

@app.post('/search/position/')
def create_position(position: schemas.Position, db: Session = Depends(get_db)):
    new_position = models.Position(Position=position.Position)
    db.add(new_position)
    db.commit()
    db.refresh(new_position)
    return {'message': 'Position added successfully'}

@app.delete('/search/position/{position_id}')
def delete_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(models.Position).get(position_id)
    if position:
        db.delete(position)
        db.commit()
        return {'message': 'Position deleted successfully'}
    else:
        raise HTTPException(status_code=404, detail='Position not found')

@app.get('/search/connection_search', response_model=List[schemas.Search])
def get_all_searches(db: Session = Depends(get_db)):
    searches = db.query(models.Search).all()
    return [schemas.Search.from_orm(search) for search in searches]

@app.post('/search/connection_search')
def create_search(search: schemas.Search, db: Session = Depends(get_db)):
    new_search = models.Search(
        Name=search.Name,
        Note=search.Note,
        Search=search.Search,
        Connection_first_name=search.Connection_first_name,
        Connection_last_name=search.Connection_last_name,
        Connection_email=search.Connection_email,
        Connection_company=search.Connection_company,
        Connection_position=search.Connection_position,
        Connection_connection=search.Connection_connection
    )
    db.add(new_search)
    db.commit()
    db.refresh(new_search)
    return {'message': 'Search added successfully'}

@app.delete('/search/connection_search/{search_id}')
def delete_search(search_id: int, db: Session = Depends(get_db)):
    search = db.query(models.Search).get(search_id)
    if search:
        db.delete(search)
        db.commit()
        return {'message': 'Search deleted successfully'}
    else:
        raise HTTPException(status_code=404, detail='Search not found')

@app.post('/serach/company_position/')
def bard_ask(ask: schemas.SearchCompanyPosition):
    try:
        result = make_search(ask.company, ask.position, ask.email, ask.password,driver,0)#subprocess.check_output(["python", "scripts/newsearch.py", ask.company, ask.position, ask.email, ask.password], stderr=subprocess.STDOUT, text=True)
        return {"response": result}
    except subprocess.CalledProcessError as e:
        return {"response": str(e.output)}
    