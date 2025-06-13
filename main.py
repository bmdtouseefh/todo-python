from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import  Todo, Session, Priority, SessionLocal, update,delete, select
from pydantic import BaseModel, Field
from typing import Optional, List

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

@app.get("/todos")

def getTodos(first_n: int = None, db: Session = Depends(get_db)):
    if first_n != None:
        stmt = select(Todo).order_by(Todo.id).limit(first_n)
        todoList = db.scalars(stmt).all()
        return todoList

    else:
        stmt = select(Todo)
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
    try:
        if updatedTodo.name!=None:
            stmt = (update(Todo).where(Todo.id == todo_id).values(name=updatedTodo.name))
            db.execute(stmt)
            db.commit()
        elif updatedTodo.desc != None: 
            stmt = (update(Todo).where(Todo.id == todo_id).values(desc=updatedTodo.name))
            db.execute(stmt)
            db.commit()
        elif updatedTodo.priority != None: 
            stmt = (update(Todo).where(Todo.id == todo_id).values(priority=updatedTodo.name))
            db.execute(stmt)
            db.commit()
        elif updatedTodo.completed != None: 
            stmt = (update(Todo).where(Todo.id == todo_id).values(completed=updatedTodo.completed))
            db.execute(stmt)
            db.commit()
        return updatedTodo
    except:
        raise HTTPException(status_code=404, detail="todo item not found")

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