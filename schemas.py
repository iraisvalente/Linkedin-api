from typing import List, Optional
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
    First_Name: Optional[str]
    Last_Name: Optional[str]
    Email_Address: Optional[str]
    Company: Optional[str]
    Position: Optional[str]
    Connection: Optional[str]
    
    class Config: 
        orm_mode =True

class Position(BaseModel): 
    Position: str
    Count: Optional[str]
    
    class Config: 
        orm_mode =True
        
class Company(BaseModel): 
    Company: str
    Count: Optional[str]
    
    class Config: 
        orm_mode =True
        
class CommonConnection(BaseModel): 
    Connection: str
    Count: str
    
    class Config: 
        orm_mode =True

class Analytics(BaseModel):
    Company: str
    Positions: List[Position]
    
class Count(BaseModel):
    Count: int
    
    class Config:
        orm_mode = True

class Bard(BaseModel):
    company: str
    position: str
    
    class Config:
        orm_mode = True
        
class Linked(BaseModel):
    username: str
    password: Optional[str]
    
    class Config:
        orm_mode = True
        