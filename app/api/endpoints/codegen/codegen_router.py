from fastapi import APIRouter
from pydantic import BaseModel

from app.api.endpoints.codegen.codegen_service import CodeGenService

router = APIRouter()
_codegen_service = CodeGenService()


class RequestCodeBody(BaseModel):
    """Pydantic model for the request body for code generation.

    Attributes:
        repoUrl (str): The URL of the repository for which to generate code.
        prompt (str): The prompt based on which code will be generated.
    """
    repoUrl: str
    prompt: str


@router.post("/codegen/")
async def request_codegen(body: RequestCodeBody) -> CodeGenService.RequestCodeGenRes:
    """Request code generation based on a repository URL and a prompt.

    Args:
        body (RequestCodeBody): The request body containing the repository URL and prompt.

    Returns:
        CodeGenService.RequestCodeGenRes: An instance of the RequestCodeGenRes class containing the result of the code generation.
    """
    return _codegen_service.request_codegen(body.repoUrl, body.prompt)
