import json
import logging
import pytest
from unittest.mock import Mock, patch
from app.api.endpoints.codegen.codegen_service import CodeGenService
from app.lib.codegen.models import CodeGenResult, CodeGenHistoryItem, CodeGenPlan, CodeGenReview

# Mock the CodeGenResult object
mock_codegen_result = CodeGenResult(
    code_diff='Generated diff',
    history=[CodeGenHistoryItem(
            plan=CodeGenPlan(steps=['Step1'], file_paths=['path1']),        review=CodeGenReview(score=9, comment='Good job!'),
            code_diff='Generated diff'
        )],
    exceeded_max_attempts=False
)

# Mock the Supabase response
mock_supabase_response = {'data': 'inserted_record', 'error': None}

# Mock the logger
mock_logger = Mock()

@pytest.fixture
def service():
    return CodeGenService()

@pytest.fixture(autouse=True)
def disable_logging():
    with patch.object(logging, 'info', mock_logger):
        yield

@patch('app.lib.codegen.orchestrator.CodeGenOrchestrator.generate_code_diff', return_value=mock_codegen_result)
@patch('app.lib.supabase_client.SupabaseClient.insert_record', return_value=mock_supabase_response)
def test_request_codegen_success(mock_insert_record, mock_generate_code_diff, service):
    repo_url = 'http://test.repo'
    prompt = 'Create function'

    response = service.request_codegen(repo_url, prompt)
    
    assert isinstance(response, CodeGenService.RequestCodeGenRes)
    assert response.result == mock_codegen_result

    mock_generate_code_diff.assert_called_once_with()
    mock_insert_record.assert_called_once_with(
        'code_gen_requests',
        {
            'repo_url': repo_url,
            'prompt': prompt,
            'code_diff': mock_codegen_result.code_diff,
            'history': [json.dumps(item.to_json()) for item in mock_codegen_result.history],
            'exceeded_max_attempts': mock_codegen_result.exceeded_max_attempts,
        }
    )
