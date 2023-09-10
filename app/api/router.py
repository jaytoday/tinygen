from fastapi import APIRouter

from app.api.endpoints.users import users_router
from app.api.endpoints.codegen import codegen_router

api_router = APIRouter()
api_router.include_router(codegen_router.router, tags=["codegen"])
api_router.include_router(users_router.router, tags=["users"])
