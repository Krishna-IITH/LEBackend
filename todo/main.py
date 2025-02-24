from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, task, authentication

app = FastAPI(
    title="TODO APP"
)
models.Base.metadata.create_all(engine)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(authentication.router)
