from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, sessionmaker
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine, select

from enum import IntEnum

from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass

class Priority(IntEnum):
    LOW = 3,
    MEDIUM = 2,
    HIGH = 1
    
class Todo(Base):
    __tablename__ = "all_todos_3"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    desc: Mapped[str]
    priority: Mapped[Priority]
    def __repr__(self) -> str:
        return f"Todo(id={self.id!r}, name={self.name!r}, desc={self.desc!r}), priority={self.priority!r}"

    

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:sec1122@localhost/postgres'
    
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)



# todoList = session.scalars(stmt).all()
# for todo in todoList:
#     print(todo.name) 