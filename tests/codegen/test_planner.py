import json
import pytest
from unittest.mock import patch, Mock
from app.lib.codegen.planner import CodeGenPlanner
from app.common.exceptions import ApiError
from app.lib.codegen.models import CodeGenReview, CodeGenPlan

# Sample Data
sample_repo_file_map = {'file1': 'content1', 'file2': 'content2'}
sample_prompt = "Create a function that sorts an array"
sample_code_diff = "Added a sort function"
sample_steps = ["Step1", "Step2"]
sample_openai_model = "gpt-4"

# Mocking OpenAI API response
mock_response_with_data = Mock(choices=[{
    "message": {
        "function_call": {
            "arguments": json.dumps({
                "review": {"score": 0.8, "comment": "Good"},
                "plan": {"steps": ["Step3"], "file_paths": ["file3"]}
            })
        }
    }
}])

mock_response_empty = Mock(choices=[])


@pytest.fixture
def planner():
    return CodeGenPlanner(sample_prompt, sample_repo_file_map, sample_code_diff, sample_steps, sample_openai_model)


@patch('openai.ChatCompletion.create', return_value=mock_response_with_data)
def test_review_and_plan_success(mock_openai, planner):
    review, plan = planner.review_and_plan()
    
    assert isinstance(review, CodeGenReview)
    assert review.score == 0.8
    assert review.comment == "Good"
    
    assert isinstance(plan, CodeGenPlan)
    assert plan.steps == ["Step3"]
    assert plan.file_paths == ["file3"]
    
    mock_openai.assert_called_once()


@patch('openai.ChatCompletion.create', return_value=mock_response_empty)
def test_review_and_plan_api_error(mock_openai, planner):
    with pytest.raises(ApiError, match="Failed to get plan from API"):
        planner.review_and_plan()
    mock_openai.assert_called_once()


@patch('openai.ChatCompletion.create', side_effect=Exception("Random Exception"))
def test_review_and_plan_random_exception(mock_openai, planner):
    with pytest.raises(Exception, match="Random Exception"):
        planner.review_and_plan()
    mock_openai.assert_called_once()


@patch('openai.ChatCompletion.create', return_value=mock_response_with_data)
def test_review_and_plan_json_decode_error(mock_openai, planner):
    with patch('json.loads', side_effect=json.JSONDecodeError("Error", "Doc", 1)):
        with pytest.raises(ApiError, match="Failed to decode codegen planner JSON response from API"):
            planner.review_and_plan()
    mock_openai.assert_called_once()
