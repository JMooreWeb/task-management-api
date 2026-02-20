from fastapi import APIRouter
from app.api.v1 import auth, users, tasks, roles, user_roles

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/v1/users", tags=["Users"])
api_router.include_router(user_roles.router, prefix="/v1", tags=["Users"])
api_router.include_router(tasks.router, prefix="/v1/tasks", tags=["Tasks"])
api_router.include_router(roles.router, prefix="/v1/roles", tags=["Roles"])