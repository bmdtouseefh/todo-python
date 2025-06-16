from thetoken import SECRET_KEY, ALGO
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from auth import verify_password
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import  Session, SessionLocal, update,delete, select
from pydantic import BaseModel, Field
from typing import Optional, List
from models import Todo, Priority, User
from auth import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from thetoken import create_token

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # Create React App
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
        allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserCreate(BaseModel):
    username: str = Field(..., description='username')
    email: str = Field(..., description=" New email ")
    password: str = Field(..., description="user password")

class TodoBase(BaseModel):
    name: str = Field(..., description="Task Name")
    desc: str = Field(..., description="Task Desc")
    priority: Priority = Field(default=Priority.LOW, )
    
class TodoRead(TodoBase):
     id: int = Field(..., description="Unique identifier, will be auto created")
     class Config:
         orm_mode = True

class CreateTodo(TodoBase):
     pass

class UpdateTodo(TodoBase):
    name: Optional[str] = Field(None, description="new task name")
    desc: Optional[str] = Field(None, description="udpated desc")
    priority: Optional[int] = Field(None, description="updated priority")
    completed: Optional[bool]




    

@app.get("/")
def index():
    return "Hello World"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        email: str = payload.get("sub")
        user = db.query(User).filter(User.email==email).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/todos")

def getTodos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = (Todo).where(Todo.owner_id == current_user.id)
    todoList = db.scalars(stmt).all()
    return todoList




@app.post("/createtodo")
def createTodo(newTodo: CreateTodo, db: Session = Depends(get_db)):
    stmt = select(Todo).order_by(Todo.id)
    todoList = db.scalars(stmt).all()
    id = len(todoList)+1
    theTodo=Todo(
        id=id,
        name=newTodo.name,
        desc=newTodo.desc,
        priority=newTodo.priority,
        completed=False
    )
    db.add(theTodo)
    db.commit()
    db.refresh(theTodo) 
    todoList = db.scalars(stmt).all()
    return todoList

@app.put("/updatetodo/{todo_id}")
def updateTodo(todo_id: int,updatedTodo: UpdateTodo, db: Session = Depends(get_db)):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")


    if updatedTodo.name!=None:
        stmt = (update(Todo).where(Todo.id == todo_id).values(name=updatedTodo.name))
        db.execute(stmt)
        db.commit()
    if updatedTodo.desc != None: 
        stmt = (update(Todo).where(Todo.id == todo_id).values(desc=updatedTodo.desc))
        db.execute(stmt)
        db.commit()
    if updatedTodo.priority != None and updatedTodo.priority in Priority: 
        stmt = (update(Todo).where(Todo.id == todo_id).values(priority=updatedTodo.priority))
        db.execute(stmt)
        db.commit()
    if updatedTodo.completed != None: 
        stmt = (update(Todo).where(Todo.id == todo_id).values(completed=updatedTodo.completed))
        db.execute(stmt)
        db.commit()
        return updatedTodo




@app.delete("/deltodo/{todo_id}")
def deleteTodo(todo_id: int, db: Session = Depends(get_db)):
    try:
        item=db.scalar(select(Todo).where(Todo.id ==todo_id))
        print(item)
        stmt = (delete(Todo).where(Todo.id == todo_id))
        db.execute(stmt)
        db.commit()
        return item
    except:
        raise HTTPException(status_code=404, detail="todo item not found")
    


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    add_user = User(email=user.email, hashed_password=hashed_pw, username=user.username)
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    return {"registered": user}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user=db.query(User).filter(User.email==form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_token(data={"sub":user.email})
    return ({"access token": token, "token_type": "bearer"})

