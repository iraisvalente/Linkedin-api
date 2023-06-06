from sqlalchemy import Column, Integer, String
from connection import Base

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer,primary_key=True,index=True)
    First_Name = Column(String(255))
    Last_Name = Column(String(255))
    Email_Address = Column(String(255))
    Company = Column(String(255))
    Position = Column(String(255))
    Password_user = Column(String(255))
    
class Connection(Base):
    __tablename__ = 'Connections'
    First_Name = Column(String(255),primary_key=True)
    Last_Name = Column(String(255))
    Email_Address = Column(String(255))
    Company = Column(String(255))
    Position = Column(String(255))
    Connection = Column(String(255))