from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    First_Name:str| None
    Last_Name:str| None
    Email_Address:str| None
    Company:str| None
    Position:str| None
    Password_user:str| None

    class Config:
        orm_mode =True
    
class Connection(BaseModel):
    First_Name:str| None
    Last_Name:str| None
    Email_Address:str| None
    Company:str| None
    Position:str| None
    Connection:str| None
    
    class Config:
        orm_mode =True