import os
from typing import Optional

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

def _truncate_diff(diff: str, max_chars: int = 8000) -> str:
    """Cắt diff nếu quá dài, giữ phần đầu và cuối."""
    if len(diff) <= max_chars:
        return diff
    half = max_chars // 2
    return diff[:half] + "\n... [truncated] ...\n" + diff[-half:]

def generate_message_with_gemini(diff: str, style: str = "conventional") -> Optional[str]:
    if not GEMINI_AVAILABLE:
        return None
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    diff = _truncate_diff(diff, 8000)
    prompt = f"""You are an expert Git commit message writer.
Given the following git diff, write a concise, informative commit message in Conventional Commits format (e.g., feat: add login, fix: resolve bug, docs: update readme).
Style: {style}
Diff:
{diff}
Output ONLY the commit message, no extra text, no markdown."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None

def generate_message_with_openai(diff: str, style: str = "conventional") -> Optional[str]:
    if not OPENAI_AVAILABLE:
        return None
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    client = OpenAI(api_key=api_key)
    diff = _truncate_diff(diff, 4000)
    prompt = f"Write a git commit message (Conventional Commits format) for this diff:\n\n{diff}\n\nStyle: {style}\nMessage:"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None

def generate_commit_message(diff: str, style: str = "conventional", provider: str = "gemini") -> Optional[str]:
    if provider == "gemini":
        return generate_message_with_gemini(diff, style)
    elif provider == "openai":
        return generate_message_with_openai(diff, style)
    else:
        return None
