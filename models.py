

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, sessionmaker
from sqlalchemy.orm import mapped_column
from enum import IntEnum
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass

class Priority(IntEnum):
    LOW = 3,
    MEDIUM = 2,
    HIGH = 1
    
class Todo(Base):
    __tablename__ = "all_todos_3"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    desc: Mapped[str]
    priority: Mapped[Priority]
    completed: Mapped[bool]
    def __repr__(self) -> str:
        return f"Todo(id={self.id!r}, name={self.name!r}, desc={self.desc!r}), priority={self.priority!r}"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r},email={self.email!r}, username={self.username!r})"