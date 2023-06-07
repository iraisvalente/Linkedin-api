from typing import Optional
from pydantic import BaseModel

class User(BaseModel): 
    First_Name: str
    Last_Name: str
    Email_Address: str
    Company: str
    Position: str
    Password_user: str

    class Config: 
        orm_mode =True
    
class Connection(BaseModel): 
    First_Name: str
    Last_Name: str
    Email_Address: str
    Company: str
    Position: str
    Connection: str
    
    class Config: 
        orm_mode =True

class Position(BaseModel): 
    Position: str
    Count: str
    
    class Config: 
        orm_mode =True
        
class Company(BaseModel): 
    Company: str
    Count: str
    
    class Config: 
        orm_mode =True
        
class Connection(BaseModel): 
    Connection: str
    Count: str
    
    class Config: 
        orm_mode =True