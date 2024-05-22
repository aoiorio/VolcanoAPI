from fastapi import APIRouter

from .endpoints.todo import router as todo_router

routes = APIRouter()

routes.include_router(todo_router)


