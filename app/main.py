from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import Engine
from .routers import post, user, like
from .config import setting

app = FastAPI()

origins = ["*"]

app.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
)
models.Base.metadata.create_all(bind=Engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(like.router)

#@Home
@app.get("/")
async def root():
        return "Fast API Testin"