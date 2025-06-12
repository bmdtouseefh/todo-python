from fastapi import FastAPI, HTTPException
from enum import IntEnum
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

class Priority(IntEnum):
    LOW = 3,
    MEDIUM = 2,
    HIGH = 1


class TodoBase(BaseModel):
    name: str = Field(..., description="Task Name")
    desc: str = Field(..., description="Task Desc")
    priority: Priority = Field(default=Priority.LOW, )
    
class Todo(TodoBase):
     id: int = Field(..., description="Unique identifier, will be auto created")

class CreateTodo(TodoBase):
     pass

class UpdateTodo(TodoBase):
    name: Optional[str] = Field(..., description="new task name")
    desc: Optional[str] = Field(..., description="udpated desc")
    priority: Optional[int] = Field(..., description="updated priority")


all_todos=[
     
     Todo(id=1, name="sports", desc="running", priority=2),
     Todo(id=2, name="watch",desc="tutorial", priority=3)
    
]

@app.get("/")
def index():
    return "Hello World"

@app.get("/todos", response_model=List[Todo])
def getTodos(first_n: int = None):
    if first_n != None:
        return all_todos[:first_n]
    else:
        return all_todos

@app.post("/createtodo", response_model=Todo)
def createTodo(newTodo: CreateTodo):
    id = len(all_todos)+1
    theTodo=Todo(
        id=id,
        name=newTodo.name,
        desc=newTodo.desc,
        priority=newTodo.priority
    )
    all_todos.append(theTodo)
    return theTodo

@app.put("/updatetodo/{todo_id}", response_model=Todo)
def updateTodo(todo_id: int,updatedTodo: UpdateTodo):
    for todo in all_todos:
        if todo.id == todo_id:
            todo.name=updatedTodo.name
            todo.desc=updatedTodo.desc
            todo.priority=updatedTodo.priority
            return todo
    raise HTTPException(status_code=404, detail="todo item not found")

@app.delete("/deleteto/{todo_id}", response_model=Todo)
def deleteTodo(todo_id: int):
    for index,todo in enumerate(all_todos):
        if todo.id == todo_id:
            all_todos.pop(index)
            return todo
    raise HTTPException(status_code=404, detail="not found")