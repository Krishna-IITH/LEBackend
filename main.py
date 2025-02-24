from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Task(BaseModel):
    title: str
    status: str
    priority: str
    created_at: Optional[bool]

@app.get('/')
def dashboard():
    return {'status':200, 'data': 'Dashboard'}

@app.get('/tasks')
def tasks_list(limit=10):
    return {'status':200, 'data': f'{limit} Tasks List'}

@app.get('/task/{id}')
def task_detail(id):
    return {'status': 200, 'data': id}

@app.post('/task')
def task_create(request: Task):
    return request
    # return {'status': 200, 'data': 'Task created sucessfully'}

