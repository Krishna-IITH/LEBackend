from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, task, authentication
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI(
    title="TODO APP"
)
models.Base.metadata.create_all(engine)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(authentication.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=500
)