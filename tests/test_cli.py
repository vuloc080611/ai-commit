import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from ai_commit.cli import cli

@patch("ai_commit.cli.is_git_repo")
def test_cli_outside_git_repo(mock_is_git_repo):
    mock_is_git_repo.return_value = False
    runner = CliRunner()
    result = runner.invoke(cli, ["suggest"])
    assert result.exit_code == 1
    assert "Not a git repository" in result.output

@patch("ai_commit.cli.is_git_repo", return_value=True)
@patch("ai_commit.cli.get_git_diff")
@patch("ai_commit.cli.generate_commit_message")
def test_suggest_no_changes(mock_gen, mock_diff, mock_git_repo):
    mock_diff.return_value = None
    runner = CliRunner()
    result = runner.invoke(cli, ["suggest"])
    assert "No staged changes" in result.output
    mock_gen.assert_not_called()

@patch("ai_commit.cli.is_git_repo", return_value=True)
@patch("ai_commit.cli.get_git_diff", return_value="fake diff")
@patch("ai_commit.cli.generate_commit_message", return_value="feat: new feature")
@patch("ai_commit.cli.run_git_commit", return_value=True)
@patch("click.confirm", return_value=True)
def test_suggest_commit_yes(mock_confirm, mock_commit, mock_gen, mock_diff, mock_git_repo):
    runner = CliRunner()
    result = runner.invoke(cli, ["suggest"])
    assert "Suggested commit message" in result.output
    mock_commit.assert_called_once_with("feat: new feature")

@patch("ai_commit.cli.is_git_repo", return_value=True)
@patch("ai_commit.cli.stage_all_changes", return_value=True)
@patch("ai_commit.cli.get_git_diff", return_value="diff")
@patch("ai_commit.cli.generate_commit_message", return_value="chore: auto")
@patch("ai_commit.cli.run_git_commit", return_value=True)
def test_commit_command(mock_commit, mock_gen, mock_diff, mock_stage, mock_git_repo):
    runner = CliRunner()
    result = runner.invoke(cli, ["commit"])
    assert "Committed with message" in result.output
    mock_stage.assert_called_once()
    mock_commit.assert_called_once_with("chore: auto")

@patch("ai_commit.cli.is_git_repo", return_value=True)
@patch("ai_commit.cli.install_prepare_commit_msg_hook", return_value=True)
def test_install_hook(mock_install, mock_git_repo):
    runner = CliRunner()
    result = runner.invoke(cli, ["install-hook"])
    assert "Git hook installed" in result.output
