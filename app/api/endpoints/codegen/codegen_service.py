import logging
from pydantic import BaseModel

from app.lib.codegen.models import CodeGenResult
from app.lib.codegen.orchestrator import CodeGenOrchestrator
from app.lib.supabase_client import SupabaseClient


class CodeGenService:
    """Service class for code generation.

    Attributes:
        supabase_client: An instance of the SupabaseClient class.
    """

    def __init__(self):
        """Initialize the CodeGenService class with a Supabase client."""
        self.supabase_client = SupabaseClient()

    class RequestCodeGenRes(BaseModel):
        """Pydantic model for the code generation request response.

        Attributes:
            result (CodeGenResult): The result of the code generation request.
        """
        result: CodeGenResult

    def request_codegen(self, repo_url: str, prompt: str) -> RequestCodeGenRes:
        """Request code generation based on a repository URL and a prompt.

        Args:
            repo_url (str): The URL of the repository for which to generate code.
            prompt (str): The prompt based on which code will be generated.

        Returns:
            RequestCodeGenRes: An instance of the RequestCodeGenRes class containing the result of the code generation.
        """
        logging.info(f"Requesting codegen for repo: {repo_url} and prompt: {prompt}")

        codegen_orchestrator = CodeGenOrchestrator(repo_url, prompt)
        result = codegen_orchestrator.generate_code_diff()

        # Save record to Supabase
        subabase_response = self.supabase_client.insert_record(
            'code_gen_requests',
            {
                'repo_url': repo_url,
                'prompt': prompt,
                'code_diff': result.code_diff,
                'history': [history_item.to_json() for history_item in result.history],
                'exceeded_max_attempts': result.exceeded_max_attempts,
            }
        )
        logging.info(f"Supabase response: {subabase_response}")

        return self.RequestCodeGenRes(result=result)
