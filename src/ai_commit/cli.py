import click
import sys
from ai_commit.git_utils import (
    get_git_diff, is_git_repo, run_git_commit, stage_all_changes,
    install_prepare_commit_msg_hook
)
from ai_commit.commit_gen import generate_commit_message

@click.group()
def cli():
    """AI Commit – intelligent commit messages using Gemini/OpenAI."""
    if not is_git_repo():
        click.secho("❌ Not a git repository. Please run inside a git repo.", fg="red")
        sys.exit(1)

@cli.command()
@click.option("--style", default="conventional", help="Style: conventional, funny, poetic, short, etc.")
@click.option("--provider", default="gemini", help="AI provider: gemini or openai")
@click.option("--hook", is_flag=True, help="Internal use for git hook (no interactive prompt)")
def suggest(style, provider, hook):
    """Suggest a commit message based on staged changes."""
    diff = get_git_diff(staged_only=True)
    if not diff:
        click.secho("⚠️  No staged changes. Run `git add` first or use `ai-commit commit` to auto-stage all.", fg="yellow")
        return
    click.echo("🔍 Analyzing diff with AI...")
    msg = generate_commit_message(diff, style, provider)
    if not msg:
        click.secho("❌ Failed to generate message. Check your API key and internet connection.", fg="red")
        return
    click.secho("\n✨ Suggested commit message:\n", fg="green")
    click.echo(msg)
    if not hook:
        if click.confirm("\nDo you want to use this message and commit now?"):
            if run_git_commit(msg):
                click.secho("✅ Commit successful!", fg="green")
            else:
                click.secho("❌ Commit failed. Make sure you have staged changes.", fg="red")

@cli.command()
@click.option("--style", default="conventional")
@click.option("--provider", default="gemini")
def commit(style, provider):
    """Automatically stage all changes and commit with AI message."""
    click.echo("📦 Staging all changes...")
    if not stage_all_changes():
        click.secho("❌ Failed to stage changes.", fg="red")
        return
    diff = get_git_diff(staged_only=True)
    if not diff:
        click.secho("⚠️  No changes to commit after staging.", fg="yellow")
        return
    click.echo("🤖 Generating commit message...")
    msg = generate_commit_message(diff, style, provider)
    if not msg:
        click.secho("❌ Generation failed.", fg="red")
        return
    if run_git_commit(msg):
        click.secho(f"✅ Committed with message: {msg}", fg="green")
    else:
        click.secho("❌ Commit failed.", fg="red")

@cli.command()
def install_hook():
    """Install git prepare-commit-msg hook to auto-suggest messages."""
    if install_prepare_commit_msg_hook():
        click.secho("✅ Git hook installed. Next time you run `git commit`, ai-commit will suggest a message.", fg="green")
    else:
        click.secho("❌ Failed to install hook. Check permissions.", fg="red")
