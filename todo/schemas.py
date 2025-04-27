from pydantic import BaseModel
from typing import List, Optional
import enum

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
    # token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# class Grade(enum.Enum):
#     A_PLUS = "a+"
#     A = "a"
#     B = "b"
#     C = "c"
#     D = "d"
#     F = "f"


class Resources(BaseModel):
    Websites: str
    Videos: str
    Books: str


class Explaination(BaseModel):
  topic: str
  explaination: str
  simulation: str
  resources: Resources



class Step(BaseModel):
    id: int
    title: str
    description: str
    svg_code: str
    order: int


class GuidedExplanation(BaseModel):
    steps: list[Step]


class PromptRequest(BaseModel):
    prompt: str
    

class TopicRequest(BaseModel):
    topic: str