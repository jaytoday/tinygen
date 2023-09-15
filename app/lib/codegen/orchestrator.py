import logging
from typing import List

import openai
from decouple import config

from app.lib.codegen.models import CodeGenHistoryItem, CodeGenPlan, CodeGenReview, CodeGenResult
from app.lib.codegen.planner import CodeGenPlanner
from app.lib.codegen.utils import MAX_PLANNING_ATTEMPTS, SUCCESS_SCORE_THRESHOLD, chunk_file_contents
from app.lib.codegen.worker import CodeGenWorker
from app.lib.filesystem import (
    fetch_file_map,
    fetch_files,
    generate_hash_for_repo_and_prompt,
    prepare_temp_dir,
    remove_temp_dir,
)
from app.lib.github import fetch_github_repo_contents

DEFAULT_OPENAI_MODEL = config("OPENAI_MODEL", "gpt-4")

# Load API key from .env file
openai.api_key = config("OPENAI_API_KEY")


class CodeGenOrchestrator:
    """Orchestrator for code generation based on a given repository URL and a prompt.

    Attributes:
        openai_model (str): The model to be used for OpenAI API calls.
        repo_url (str): The URL of the GitHub repository.
        prompt (str): The prompt describing what code should be generated.
    """

    def __init__(self, repo_url: str, prompt: str, openai_model=DEFAULT_OPENAI_MODEL):
        self.openai_model = openai_model
        self.repo_url = repo_url
        self.prompt = prompt

    def generate_code_diff(self) -> CodeGenResult:
        """Generate a code difference based on the GitHub repository and a given prompt.

        Returns:
            CodeGenResult: An object containing the generated code diff, whether max attempts were exceeded,
                           and the history of code generation steps.
        """
        review: CodeGenReview
        plan: CodeGenPlan
        code_diff: str = None
        previous_steps: List[str] = None
        attempts = 0
        history: List[CodeGenHistoryItem] = []

        logging.info(f"Generating code diff for repo: {self.repo_url} and prompt: {self.prompt}")

        repo_hash = generate_hash_for_repo_and_prompt(self.repo_url, self.prompt)
        repo_dir = prepare_temp_dir(repo_hash)
        fetch_github_repo_contents(self.repo_url, repo_dir)
        repo_file_map = fetch_file_map(repo_dir)

        while attempts <= MAX_PLANNING_ATTEMPTS:
            attempts += 1
            logging.info(f"Planning attempt {attempts} of {MAX_PLANNING_ATTEMPTS}")

            planner = CodeGenPlanner(self.prompt, repo_file_map, code_diff, previous_steps, self.openai_model)
            review, plan = planner.review_and_plan()

            if (review and review.score >= SUCCESS_SCORE_THRESHOLD) or \
                    (plan and len(plan.steps) == 0) or \
                    (attempts > MAX_PLANNING_ATTEMPTS):
                history.insert(0, CodeGenHistoryItem(plan=plan, review=review, code_diff=None))
                logging.debug("breaking out of while loop")
                break

            file_contents = fetch_files(repo_dir, plan.file_paths)
            chunked_contents = chunk_file_contents(file_contents)

            code_diff_chunks: List[str] = []
            for content_chunk in chunked_contents:
                worker = CodeGenWorker(content_chunk, plan.steps, self.openai_model)
                code_diff_chunk = worker.generate_code_diff()
                code_diff_chunks.append(code_diff_chunk)

            code_diff = "\n".join(code_diff_chunks)
            history.insert(0, CodeGenHistoryItem(plan=plan, review=review, code_diff=code_diff))
            previous_steps = plan.steps

        remove_temp_dir(repo_dir)  # cleanup

        logging.info(f"Returning code diff: {code_diff}")

        return CodeGenResult(
            code_diff=code_diff,
            exceeded_max_attempts=(attempts > MAX_PLANNING_ATTEMPTS),
            history=history
        )
