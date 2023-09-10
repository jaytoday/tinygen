import pytest
from unittest.mock import patch, Mock
from app.lib.codegen.models import CodeGenPlan, CodeGenReview, CodeGenHistoryItem, CodeGenResult
from app.lib.codegen.orchestrator import CodeGenOrchestrator

# Mock successful review and plan
mock_review = CodeGenReview(score=9, comment="Good job!")
mock_plan = CodeGenPlan(steps=["Step1"], file_paths=["path1"])

# Mock unsuccessful review
mock_unsuccessful_review = CodeGenReview(score=2, comment="Needs improvement!")

# Mock fetch_files
mock_files = "some file content"

# Mock fetch_file_map
mock_file_map = {"path1": "file1"}


@patch('app.lib.codegen.orchestrator.prepare_temp_dir', return_value="/tmp/repo")
@patch('app.lib.codegen.orchestrator.fetch_github_repo_contents')
@patch('app.lib.codegen.orchestrator.fetch_file_map', return_value=mock_file_map)
@patch('app.lib.codegen.orchestrator.fetch_files', return_value=mock_files)
@patch('app.lib.codegen.orchestrator.CodeGenWorker')
@patch('app.lib.codegen.orchestrator.CodeGenPlanner')
def test_generate_code_diff_success(mockCodeGenPlanner, mockCodeGenWorker, mock_fetch_files,
                                    mock_fetch_file_map, mock_fetch_github_repo_contents, mock_prepare_temp_dir):
    # Setup
    mockCodeGenPlanner.return_value.review_and_plan.return_value = (mock_review, mock_plan)
    mockCodeGenWorker.return_value.generate_code_diff.return_value = "generated code"
    orchestrator = CodeGenOrchestrator("https://github.com/user/repo", "generate function to add numbers")

    # Run
    result = orchestrator.generate_code_diff()

    # Validate
    assert isinstance(result, CodeGenResult)
    assert result.exceeded_max_attempts is False
    assert len(result.history) == 2  # Initial and final history item


@patch('app.lib.codegen.orchestrator.prepare_temp_dir', return_value="/tmp/repo")
@patch('app.lib.codegen.orchestrator.fetch_github_repo_contents')
@patch('app.lib.codegen.orchestrator.fetch_file_map', return_value=mock_file_map)
@patch('app.lib.codegen.orchestrator.fetch_files', return_value=mock_files)
@patch('app.lib.codegen.orchestrator.CodeGenWorker')
@patch('app.lib.codegen.orchestrator.CodeGenPlanner')
def test_generate_code_diff_failure(mockCodeGenPlanner, mockCodeGenWorker, mock_fetch_files,
                                    mock_fetch_file_map, mock_fetch_github_repo_contents, mock_prepare_temp_dir):
    # Setup
    mockCodeGenPlanner.return_value.review_and_plan.return_value = (mock_unsuccessful_review, mock_plan)
    orchestrator = CodeGenOrchestrator("https://github.com/user/repo", "generate function to add numbers")

    # Run
    result = orchestrator.generate_code_diff()

    # Validate
    assert isinstance(result, CodeGenResult)
    assert result.exceeded_max_attempts is False
    assert len(result.history) == 1  # Only the final history item

