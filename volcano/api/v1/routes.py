from fastapi import APIRouter

from .endpoints.todo import router as todo_router
from .endpoints.auth import router as auth_router
from .endpoints.user import router as user_router

routes = APIRouter()

routes.include_router(todo_router)
routes.include_router(auth_router)
routes.include_router(user_router)


