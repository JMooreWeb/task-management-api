from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import register_routes
from app.api.router import api_router
from app.core.config import settings
from app.logger import configure_logging, LogLevels
#from app.db import init_db


configure_logging(LogLevels.info)


def create_app() -> FastAPI:
    api = FastAPI(
        title="Task Management API", 
        version="1.0.0",
        description="A simple task management API built with FastAPI, SQLAlchemy, PostgreSQL, and JWT authentication.",
        docs_url="/docs" if settings.ENV != "prod" else None,
        redoc_url="/redoc" if settings.ENV != "prod" else None,
        openapi_url="/openapi.json" if settings.ENV != "prod" else None
    )
    
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Next.js dev
            # "https://your-domain.com",  # prod
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )   
     
    api.include_router(api_router, prefix="/api/v1")
    
    return api

api = create_app()


""" Only uncomment below to create new tables, 
otherwise the tests will fail if not connected
"""
#init_db()

register_routes(api)