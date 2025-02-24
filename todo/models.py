from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    user_email = Column(String, ForeignKey('users.email'))
    creator = relationship("User", back_populates="tasks")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    tasks = relationship("Task", back_populates="creator")