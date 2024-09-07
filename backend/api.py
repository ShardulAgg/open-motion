from core import *
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime


app_router = APIRouter()

class Task(BaseModel):
    name: str
    desc: str
    priority: int
    due_date: datetime
    duration: str

@app_router.post("/add_task")
def create_task(task: Task):
    return {"message": "Task added successfully"}

@app_router.get("/")
def health_check():
    return {"status": "ok"}

__all__ = ["app_router"]