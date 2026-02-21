from fastapi import APIRouter
from app.api.v1 import auth, users, tasks, roles, user_roles

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(user_roles.router, tags=["Users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])