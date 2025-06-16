from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, sessionmaker
from sqlalchemy.orm import mapped_column
import os
from sqlalchemy import create_engine, select, update, delete
from models import Base, User

from enum import IntEnum

from sqlalchemy.orm import Session




    

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:sec1122@localhost:5432/postgres")
    
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)



# todoList = session.scalars(stmt).all()
# for todo in todoList:
#     print(todo.name) 