import datetime
from sqlalchemy import (
    DateTime, create_engine, Column, String,
    Integer, Text, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./mydb.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}   
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,    
    bind=engine
)

Base = declarative_base()

class Users(Base):
    __tablename__='user'

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    hash_pass=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.datetime.utcnow)

    message=relationship('Messages',back_populates='user')

class Messages(Base):
    __tablename__='message'

    id=Column(Integer,primary_key=True,index=True)
    sender=Column(String,nullable=False)
    receiver=Column(String,nullable=False)
    message_content=Column(Text,nullable=False)
    sender_id=Column(Integer,ForeignKey("user.id"),index=True)
    sent_at=Column(DateTime,default=datetime.datetime.utcnow)

    user=relationship('Users',back_populates='message')

Base.metadata.create_all(bind=engine)  

def get_db():        
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()