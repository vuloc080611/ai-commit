import subprocess
from pathlib import Path
from typing import Optional

def get_git_diff(staged_only: bool = True) -> Optional[str]:
    """
    Lấy diff của các thay đổi.
    Nếu staged_only=True, chỉ lấy những file đã được `git add`.
    Nếu không có staged, fallback về working directory diff.
    """
    try:
        if staged_only:
            cmd = ["git", "diff", "--cached"]
        else:
            cmd = ["git", "diff"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        diff = result.stdout.strip()
        if not diff and staged_only:
            # Fallback: không có staged, lấy working diff
            return get_git_diff(staged_only=False)
        return diff if diff else None
    except Exception:
        return None

def is_git_repo(path: Path = None) -> bool:
    """Kiểm tra thư mục hiện tại có phải git repo không."""
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run_git_commit(message: str) -> bool:
    """Thực hiện git commit với message (không tự động add)."""
    try:
        subprocess.run(["git", "commit", "-m", message], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def stage_all_changes() -> bool:
    """Chạy git add ."""
    try:
        subprocess.run(["git", "add", "."], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_prepare_commit_msg_hook() -> bool:
    """Cài đặt git hook prepare-commit-msg để gọi ai-commit suggest."""
    hook_dir = Path(".git/hooks")
    hook_dir.mkdir(exist_ok=True)
    hook_path = hook_dir / "prepare-commit-msg"
    hook_content = """#!/bin/sh
# Hook tự động sinh bởi ai-commit
if [ "$2" = "" ] && command -v ai-commit >/dev/null 2>&1; then
    ai-commit suggest --hook
fi
"""
    try:
        hook_path.write_text(hook_content)
        hook_path.chmod(0o755)
        return True
    except Exception:
        return False
