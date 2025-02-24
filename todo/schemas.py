from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    name:str
    email:str
    password:str


class Task(BaseModel):
    title: str
    status: str
    priority: str


class showUser(BaseModel):
    name:str
    email:str
    tasks: List[Task] = []
    class Config():
        from_attributes = True


class showTask(BaseModel):
    title: str
    status: str
    creator: showUser
    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None