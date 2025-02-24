from fastapi import HTTPException, status
from .. import models
from sqlalchemy.orm import Session


def get_all(db: Session):
    tasks = db.query(models.Task).all()
    return tasks


def create(request, db: Session):
    new_task = models.Task(title=request.title, status=request.status, priority=request.priority, user_email='krish@email.com')
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update(id: int, request, db: Session):
    task = db.query(models.Task).filter(models.Task.id == id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with {id} not found!')
    task.update(
        {
            'title': request.title,
            'status': request.status,
            'priority': request.priority
        }
    )
    db.commit()
    return 'Updated'


def destroy(id, db: Session):
    task = db.query(models.Task).filter(models.Task.id == id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with {id} not found!')
    task.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'


def details(id: int, db: Session):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with {id} Not Found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'Task with {id} Not Found'}
    return task