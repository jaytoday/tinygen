from fastapi import APIRouter

from app.api.endpoints.codegen import codegen_router

api_router = APIRouter()
api_router.include_router(codegen_router.router, tags=["codegen"])
