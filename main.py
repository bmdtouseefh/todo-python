from fastapi import FastAPI, HTTPException, Depends

from database import  Todo, Session, Priority, SessionLocal, select
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()




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

# class UpdateTodo(TodoBase):
#     name: Optional[str] = Field(..., description="new task name")
#     desc: Optional[str] = Field(..., description="udpated desc")
#     priority: Optional[int] = Field(..., description="updated priority")




    

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
        priority=newTodo.priority
    )
    db.add(theTodo)
    db.commit()
    db.refresh(theTodo) 
    todoList = db.scalars(stmt).all()
    return todoList

# @app.put("/updatetodo/{todo_id}", response_model=Todo)
# def updateTodo(todo_id: int,updatedTodo: UpdateTodo):
#     for todo in all_todos:
#         if todo.id == todo_id:
#             todo.name=updatedTodo.name
#             todo.desc=updatedTodo.desc
#             todo.priority=updatedTodo.priority
#             return todo
#     raise HTTPException(status_code=404, detail="todo item not found")

# @app.delete("/deleteto/{todo_id}", response_model=Todo)
# def deleteTodo(todo_id: int):
#     for index,todo in enumerate(all_todos):
#         if todo.id == todo_id:
#             all_todos.pop(index)
#             return todo
#     raise HTTPException(status_code=404, detail="not found")