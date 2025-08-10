from fastapi import FastAPI, Depends, HTTPException, Response, status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) //no need if using alembic

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def index():
    return {"data": "index"}