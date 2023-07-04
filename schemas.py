from typing import List, Optional
from pydantic import BaseModel, Field

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

    class Config:
        orm_mode = True

class PositionCount(BaseModel): 
    Position: str
    Count: Optional[str]
    
    class Config: 
        orm_mode =True
        
class CompanyCount(BaseModel): 
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
    Positions: List[PositionCount]
    
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
        
class FileRequest(BaseModel):
    name: str
    content: str
    email: str
    
    class Config:
        orm_mode = True

class Search(BaseModel):
    Name: str
    Note: str
    Search: bool 
    Connection_first_name: str
    Connection_last_name: str
    Connection_email: str
    Connection_company: str
    Connection_position: str
    Connection_connection: str
    
    class Config:
        orm_mode = True
