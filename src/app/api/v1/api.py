from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.tasks import router as tasks_router

def register_routes(api: FastAPI):
    api.include_router(auth_router)
    api.include_router(users_router)
    api.include_router(tasks_router)