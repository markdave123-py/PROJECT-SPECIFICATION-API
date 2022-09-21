from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .routers import user,login, projects,tasks
from fastapi.middleware.cors import CORSMiddleware

from . import models

from .database import engine

# models.base.metadata.create_all(bind= engine)


app = FastAPI()

origins= ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(login.router)
app.include_router(projects.router)
app.include_router(tasks.router)