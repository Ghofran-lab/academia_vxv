from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .context import DEFAULT_CONTEXT_DIR, load_context_documents, render_context
from .openai_client import generate_text
from .prompts import SYSTEM_PROMPT, WEEKLY_CONTENT_PROMPT


def build_weekly_prompt(context_dir: Path = DEFAULT_CONTEXT_DIR) -> str:
    context = render_context(load_context_documents(context_dir))
    return WEEKLY_CONTENT_PROMPT.format(academy_context=context)


def generate_weekly_content(context_dir: Path = DEFAULT_CONTEXT_DIR) -> str:
    return generate_text(build_weekly_prompt(context_dir), SYSTEM_PROMPT)


def save_generated_content(content: str, output_dir: Path = Path("content/generated")) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    path = output_dir / f"weekly_content_{stamp}.md"
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return path
