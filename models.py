from sqlalchemy import Column, Integer, String, Boolean
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

class Position(Base):
    __tablename__ = 'Positions'
     
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Position = Column(String(255))

class Search(Base):
    __tablename__ = 'Searches'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Note = Column(String(255))
    Search = Column(Boolean)
    Connection_first_name = Column(String(255))
    Connection_last_name = Column(String(255))
    Connection_email = Column(String(255))
    Connection_company = Column(String(255))
    Connection_position = Column(String(255))
    Connection_connection = Column(String(255))