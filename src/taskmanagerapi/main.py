from fastapi import FastAPI
from taskmanagerapi.routers import task, user
from taskmanagerapi.database import engine, Base
import taskmanagerapi.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)