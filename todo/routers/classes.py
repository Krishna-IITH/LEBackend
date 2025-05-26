from fastapi import APIRouter, Depends, status
from .. import schemas, oauth2
from typing import List
from ..repository import classes
from sqlalchemy.orm import Session
from ..supabase_client import supabase

router = APIRouter(
    prefix = '/class',
    tags = ['Classes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(data: schemas.MyClass):
    return classes.create(data)

# @router.get('/', response_model=List[schemas.MyClass])
@router.post('/list')
def classes_list(data: schemas.Token):
    response = (
        supabase.table("users")
        .select("email").eq("token", data.access_token)
        .execute()
    )
    return classes.get_all(response.data[0]['email'])

@router.post('/syllabus')
def class_syllabus(id: int, data: schemas.Token):
    print(data.access_token)
    response = (
        supabase.table("users")
        .select("email").eq("token", data.access_token)
        .execute()
    )
    print(response)
    return classes.get_class(response.data[0]['email'], id)