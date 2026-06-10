from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class Exercise:
    """Représentation normalisée d'un exercice exportable en Markdown."""

    source_url: str
    title: str
    statement: str
    questions: list[str] = field(default_factory=list)
    correction: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    scraped_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
