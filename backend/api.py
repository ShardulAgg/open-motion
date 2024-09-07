from core import *
from fastapi import APIRouter

app_router = APIRouter()

@app_router.post("/new_task")


@app_router.get("/")
def health_check():
    return {"status": "ok"}

__all__ = ["app_router"]