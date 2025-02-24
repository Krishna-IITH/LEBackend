from fastapi import HTTPException, status
from .. import models, hashing
from sqlalchemy.orm import Session


def create(request, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bycrpt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with {email} Not Found')
    return user