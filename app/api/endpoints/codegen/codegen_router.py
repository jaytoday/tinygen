from fastapi import APIRouter
from app.api.endpoints.codegen.codegen_service import CodeGenService
from pydantic import BaseModel


router = APIRouter()
_codegen_service = CodeGenService()


class RequestCodeBody(BaseModel):
    repoUrl: str
    prompt: str


@router.post("/codegen/")
async def request_codegen(body: RequestCodeBody) -> CodeGenService.RequestCodeGenRes:
    return _codegen_service.request_codegen(body.repoUrl, body.prompt)


@router.get("/codegen/{requestId}")
def get_codegen_request_status() -> CodeGenService.GetCodeGenRequestStatusRes:
    return _codegen_service.get_codegen_request_status()
