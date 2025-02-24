from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..repository import user


router = APIRouter(
    prefix = '/user',
    tags = ['Users']
)

get_db = database.get_db

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.showUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}', status_code=200, response_model=schemas.showUser)
def get_user(email: str, db: Session = Depends(get_db)):
    return user.get(email, db)