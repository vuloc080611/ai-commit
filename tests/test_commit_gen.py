import pytest
from unittest.mock import patch, MagicMock
from ai_commit.commit_gen import generate_commit_message, _truncate_diff

def test_truncate_diff_short():
    diff = "short diff"
    assert _truncate_diff(diff, 100) == diff

def test_truncate_diff_long():
    diff = "a" * 9000
    truncated = _truncate_diff(diff, 8000)
    assert len(truncated) <= 8000 + 30  # plus truncation message
    assert "... [truncated] ..." in truncated

@patch("ai_commit.commit_gen.generate_message_with_gemini")
def test_generate_commit_message_gemini(mock_gemini):
    mock_gemini.return_value = "feat: add login"
    result = generate_commit_message("fake diff", provider="gemini")
    assert result == "feat: add login"
    mock_gemini.assert_called_once_with("fake diff", "conventional")

@patch("ai_commit.commit_gen.generate_message_with_openai")
def test_generate_commit_message_openai(mock_openai):
    mock_openai.return_value = "fix: resolve memory leak"
    result = generate_commit_message("fake diff", provider="openai")
    assert result == "fix: resolve memory leak"

def test_generate_commit_message_invalid_provider():
    result = generate_commit_message("diff", provider="unknown")
    assert result is None
