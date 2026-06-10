from __future__ import annotations

import re
import unicodedata
from pathlib import Path


from .models import Exercise


def slugify(value: str, fallback: str = "exercice") -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or fallback


def to_markdown(exercise: Exercise) -> str:
    front_matter = {
        "title": exercise.title,
        "source_url": exercise.source_url,
        "scraped_at": exercise.scraped_at.isoformat(),
        "content_type": "exercise",
        **exercise.metadata,
    }
    yaml_block = _dump_front_matter(front_matter)
    parts = ["---", yaml_block, "---", "", f"# {exercise.title}", ""]

    if exercise.statement:
        parts.extend(["## Énoncé", "", exercise.statement.strip(), ""])

    if exercise.questions:
        parts.extend(["## Questions", ""])
        parts.extend(f"{index}. {question.strip()}" for index, question in enumerate(exercise.questions, start=1))
        parts.append("")

    if exercise.correction:
        parts.extend(["## Correction", "", exercise.correction.strip(), ""])

    parts.extend(["## Source", "", f"- {exercise.source_url}", ""])
    return "\n".join(parts)


def write_markdown(exercise: Exercise, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    base = slugify(exercise.title)
    target = output_dir / f"{base}.md"
    counter = 2
    while target.exists():
        target = output_dir / f"{base}-{counter}.md"
        counter += 1
    target.write_text(to_markdown(exercise), encoding="utf-8")
    return target


def _dump_front_matter(values: dict) -> str:
    lines: list[str] = []
    for key, value in values.items():
        if value is None:
            lines.append(f"{key}: null")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            escaped = str(value).replace('"', '\"')
            if any(char in escaped for char in [":", "#", "{", "}", "[", "]", "\n"]):
                lines.append(f'{key}: "{escaped}"')
            else:
                lines.append(f"{key}: {escaped}")
    return "\n".join(lines)
