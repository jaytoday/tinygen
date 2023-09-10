import json
import pytest
from unittest.mock import Mock, patch
from app.lib.codegen.worker import CodeGenWorker
from app.common.exceptions import ApiError

# Sample Data
sample_content_chunk = "Old content here"
sample_steps = ["Add function", "Remove comment"]
sample_openai_model = "gpt-4"

# Mocking OpenAI API response
mock_response_with_data = Mock(choices=[{
    "message": {
        "function_call": {
            "arguments": json.dumps({
                "code_diff": "New content here"
            })
        }
    }
}])

mock_response_empty = Mock(choices=[])

@pytest.fixture
def worker():
    return CodeGenWorker(sample_content_chunk, sample_steps, sample_openai_model)


@patch('openai.ChatCompletion.create', return_value=mock_response_with_data)
def test_generate_code_diff_success(mock_openai, worker):
    code_diff = worker.generate_code_diff()
    
    assert isinstance(code_diff, str)
    assert code_diff == "New content here"
    
    mock_openai.assert_called_once()


@patch('openai.ChatCompletion.create', return_value=mock_response_empty)
def test_generate_code_diff_api_error(mock_openai, worker):
    with pytest.raises(ApiError, match="Failed to get plan from API"):
        worker.generate_code_diff()
    mock_openai.assert_called_once()


@patch('openai.ChatCompletion.create', side_effect=Exception("Random Exception"))
def test_generate_code_diff_random_exception(mock_openai, worker):
    with pytest.raises(Exception, match="Random Exception"):
        worker.generate_code_diff()
    mock_openai.assert_called_once()


@patch('openai.ChatCompletion.create', return_value=mock_response_with_data)
def test_generate_code_diff_json_decode_error(mock_openai, worker):
    with patch('json.loads', side_effect=json.JSONDecodeError("Error", "Doc", 1)):
        with pytest.raises(ApiError, match="Failed to decode codegen worker JSON response from API"):
            worker.generate_code_diff()
    mock_openai.assert_called_once()
