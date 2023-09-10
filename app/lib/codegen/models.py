from typing import List, Optional
from pydantic import BaseModel


class CodeGenPlan(BaseModel):
    """Data model for representing a code generation plan.

    Attributes:
        steps (List[str]): Steps required for code generation.
        file_paths (List[str]): File paths relevant to the code generation.
    """

    steps: List[str]
    file_paths: List[str]

    def to_json(self) -> dict:
        """Convert the CodeGenPlan object to a JSON serializable dictionary.

        Returns:
            dict: A dictionary containing the serialized data.
        """
        return self.dict()


class CodeGenReview(BaseModel):
    """Data model for representing a code generation review.

    Attributes:
        score (int): Score assigned for the code generation.
        comment (str): Comment explaining the score.
    """

    score: int
    comment: str

    def to_json(self) -> dict:
        """Convert the CodeGenReview object to a JSON serializable dictionary.

        Returns:
            dict: A dictionary containing the serialized data.
        """
        return self.dict()


class CodeGenHistoryItem(BaseModel):
    """Data model for representing a code generation history item.

    Attributes:
        plan (Optional[CodeGenPlan]): Optional code generation plan.
        review (Optional[CodeGenReview]): Optional code generation review.
        code_diff (Optional[str]): Optional code difference.
    """

    plan: Optional[CodeGenPlan]
    review: Optional[CodeGenReview]
    code_diff: Optional[str]

    def to_json(self) -> dict:
        """Convert the CodeGenHistoryItem object to a JSON serializable dictionary.

        Returns:
            dict: A dictionary containing the serialized data.
        """
        return {
            "plan": self.plan.to_json() if self.plan else None,
            "review": self.review.to_json() if self.review else None,
            "code_diff": self.code_diff
        }


class CodeGenResult(BaseModel):
    """Data model for representing the final result of code generation.

    Attributes:
        code_diff (str): The generated code difference.
        exceeded_max_attempts (bool): Whether the maximum number of attempts was exceeded.
        history (List[CodeGenHistoryItem]): The history of code generation steps.
    """

    code_diff: str
    exceeded_max_attempts: bool
    history: List[CodeGenHistoryItem]


class CodeGenPlannerAIResponse(BaseModel):
    """Data model for representing the response from the Planner AI for code generation.

    Attributes:
        plan (Optional[CodeGenPlan]): Optional code generation plan.
        review (Optional[CodeGenReview]): Optional code generation review.
    """

    plan: Optional[CodeGenPlan]
    review: Optional[CodeGenReview]


class CodeGenWorkerAIResponse(BaseModel):
    """Data model for representing the response from the Worker AI for code generation.

    Attributes:
        code_diff (str): The generated code difference.
    """

    code_diff: str
