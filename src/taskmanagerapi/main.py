from fastapi import FastAPI
from taskmanagerapi.routers import task, user, auth
from taskmanagerapi.database import engine, Base
import taskmanagerapi.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)