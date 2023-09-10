from pydantic import BaseModel
from app.lib.github import fetch_github_repo_contents
from app.lib.code_diff import CodeDiffGenerator, CodeDiffResult


class CodeGenService:

    class RequestCodeGenRes(BaseModel):
        result: CodeDiffResult

    def request_codegen(self, repoUrl: str, prompt: str) -> CodeDiffResult:
        repo_contents = fetch_github_repo_contents(repoUrl)
        code_diff_generator = CodeDiffGenerator()
        result = code_diff_generator.generate(repo_contents, prompt)
        return {"result": result}
    
    class GetCodeGenRequestStatusRes(BaseModel):
        status: str

    def get_codegen_request_status(self) -> GetCodeGenRequestStatusRes:
        return {
            "status": "OK"
        }
