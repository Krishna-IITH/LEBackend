from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, schemas, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..repository import task

router = APIRouter(
    prefix = '/task',
    tags = ['Tasks']
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Task, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.create(request, db)


@router.get('/', response_model=List[schemas.showTask])
def tasks_list(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.get_all(db)


@router.get('/{id}', status_code=200, response_model=schemas.showTask)
def task_details(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.details(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def task_update(id:int, request: schemas.Task, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def task_delete(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.destroy(id, db)