from fastapi import APIRouter
from app.api.v1 import auth, users, tasks, roles, user_roles

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(user_roles.router)
api_router.include_router(tasks.router)
api_router.include_router(roles.router)