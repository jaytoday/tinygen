import json
from typing import Dict, List, Tuple

import openai

from app.common.exceptions import ApiError
from app.lib.codegen.models import CodeGenPlan, CodeGenPlannerAIResponse, CodeGenReview
from app.lib.codegen.utils import SUCCESS_SCORE_THRESHOLD
from app.lib.codegen.utils.prompts import generate_review_and_plan_prompt


class CodeGenPlanner:
    """Planner for generating code based on a given prompt and existing code.

    Attributes:
        prompt (str): The prompt describing what code should be generated.
        repo_file_map (Dict): A dictionary mapping file names to their content.
        code_diff (str): The existing code difference.
        steps (List[str]): The previous steps that have been taken.
        openai_model: The OpenAI model to be used for generating plans.
    """

    def __init__(self, prompt: str, repo_file_map: Dict, code_diff: str, steps: List[str], openai_model):
        self.prompt = prompt
        self.repo_file_map = repo_file_map
        self.code_diff = code_diff
        self.steps = steps
        self.openai_model = openai_model

    def review_and_plan(self) -> Tuple[CodeGenReview, CodeGenPlan]:
        """Generate a review of the previous execution and a new plan for future execution.

        Returns:
            Tuple[CodeGenReview, CodeGenPlan]: A tuple containing a review object and a plan object.
        """
        response = openai.ChatCompletion.create(
            model=self.openai_model,
            messages=[
                {
                    "role": "user",
                    "content": generate_review_and_plan_prompt(
                        self.prompt,
                        self.repo_file_map,
                        self.code_diff,
                        self.steps
                    )
                }
            ],
            functions=[
                {
                    "name": "get_codegen_review_and_plan",
                    "description": "Generate a review and plan for implementing a code diff based on the provided fields.",
                    "parameters": CodeGenPlannerAIResponse.schema()
                }
            ],
            function_call={"name": "get_codegen_review_and_plan"}
        )

        if len(response.choices):
            try:
                output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
            except json.JSONDecodeError:
                raise ApiError("Failed to decode codegen planner JSON response from API")

            review = None
            if output.get("review") and output["review"].get("score"):
                review = CodeGenReview(score=output["review"]["score"], comment=output["review"]["comment"])

            plan = None
            if output.get("plan") and output.get("review", {}).get("score") < SUCCESS_SCORE_THRESHOLD:
                plan = CodeGenPlan(steps=output["plan"]["steps"], file_paths=output["plan"]["file_paths"])

            return review, plan
        else:
            raise ApiError("Failed to get plan from API")
