from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import IntEnum
from typing import Optional, List

class Priority(IntEnum):
	LOW = 3,
	MEDIUM = 2,
	HIGH = 1

api = FastAPI()

class TodoBase(BaseModel):
	name: str = Field(..., min_length=3, max_length=512, description='Name of task')
	description: str = Field(..., description='description of task')
	priority: Priority = Field(default=Priority.LOW)

class TodoCreate(TodoBase):
	pass

class TodoUpdate(TodoBase):
	name:Optional[str] = Field(..., min_length=3, max_length=512, description='Name of task')
	description: Optional[str] = Field(..., description='description of task')
	priority: Optional[Priority] = Field(default=Priority.LOW)


class Todo(TodoBase):
	id: int = Field(..., description='unique identifier')


#pseudo db

all_todo = [

Todo(id=1, name='sport',description='gym',priority=Priority.LOW),
Todo(id=2, name='run',description='trail',priority=Priority.LOW),
Todo(id=3, name='watch',description='tutorial',priority=Priority.LOW),
]

@api.get('/')
def index():
	return {"message":"Hello world"}

@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id: int):
	for todo in all_todo:
		if todo.id == todo_id:
			return todo
	raise HTTPException(status_code=404, detail='No todo found')
		

@api.get('/todos', response_model=List[Todo])
def get_todos(first_n: int = None):
	if first_n:
		return all_todo[:first_n]
	elif first_n==None:
		return all_todo
	else:
		raise HTTPException(status_code=404, detail='No todo found')

	

@api.post('/todos', response_model=Todo)
def create_todo(atodo: TodoCreate):
	id = max(todo.id for todo in all_todo)+1
	new_todo = Todo(
		id=id,
		name=atodo.name,
		description=atodo.description,
		priority=atodo.priority)
	

	all_todo.append(new_todo)

	return new_todo



@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
	for todo in all_todo:
		if todo.id==todo_id:
			todo.name= updated_todo.name
			todo.description= updated_todo.description
			todo.priority= updated_todo.priority
			return todo
	raise HTTPException(status_code=404, detail='No todo found')

@api.delete('/deltodo/{id}',response_model=Todo)
def delete_todo(id: int):
	for index, todo in enumerate(all_todo):
		if todo.id==id:
			deleted_todo=all_todo.pop(index)
			return deleted_todo
	raise HTTPException(status_code=404, detail='No todo found')