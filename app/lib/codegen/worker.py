import json
from typing import Dict, List

import openai

from app.common.exceptions import ApiError, InputValidationError
from app.lib.codegen.models import CodeGenPlan, CodeGenReview, CodeGenWorkerAIResponse
from app.lib.codegen.utils.prompts import generate_code_diff_prompt


class CodeGenWorker:
    """
    Class for managing code generation tasks.

    Attributes:
        content_chunk (str): The piece of content to process.
        steps (List[str]): The steps to apply to the content.
        openai_model (str): The OpenAI model to use for code generation.

    Methods:
        generate_code_diff: Generates a code diff based on steps applied to a content chunk.
    """

    def __init__(self, content_chunk: str, steps: List[str], openai_model: str):
        """
        Initialize a CodeGenWorker instance.

        Args:
            content_chunk (str): The piece of content to process.
            steps (List[str]): The steps to apply to the content.
            openai_model (str): The OpenAI model to use for code generation.
        """
        self.content_chunk = content_chunk
        self.steps = steps
        self.openai_model = openai_model


    def generate_code_diff(self) -> str:
        """
        Generate a code diff based on the provided steps for the provided content chunk (if applicable).

        Returns:
            str: The generated code diff.
        
        Raises:
            ApiError: Raised when an API call or response processing fails.
        """
        response = openai.ChatCompletion.create(
            model=self.openai_model,
            messages=[
                {
                    "role": "user",
                    "content": generate_code_diff_prompt(
                        self.content_chunk,
                        self.steps
                    )
                }
            ],
            functions=[
                {
                    "name": "get_codegen_code_diff",
                    "description": (
                        "Generate a code diff for the provided code chunk "
                        "based on the provided steps. Return an empty string if no code diff is needed."
                    ),
                    "parameters": CodeGenWorkerAIResponse.schema()
                }
            ],
            function_call={"name": "get_codegen_code_diff"}
        )

        if len(response.choices):
            try:
                output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
            except json.decoder.JSONDecodeError:
                raise ApiError("Failed to decode codegen worker JSON response from API")
            return output["code_diff"]
        else:
            raise ApiError("Failed to get plan from API")
