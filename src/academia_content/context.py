from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONTEXT_DIR = Path("content/academy_context")


@dataclass(frozen=True)
class ContextDocument:
    path: Path
    content: str

    @property
    def title(self) -> str:
        return self.path.stem.replace("_", " ").replace("-", " ").title()


def load_context_documents(context_dir: Path = DEFAULT_CONTEXT_DIR) -> list[ContextDocument]:
    """Charge les fichiers Markdown qui décrivent l'académie.

    Les fichiers sont triés pour produire un prompt stable et testable.
    """
    if not context_dir.exists():
        return []
    documents: list[ContextDocument] = []
    for path in sorted(context_dir.glob("*.md")):
        if path.name == "README.md" or path.name.endswith(".example.md"):
            continue
        content = path.read_text(encoding="utf-8").strip()
        if content:
            documents.append(ContextDocument(path=path, content=content))
    return documents


def render_context(documents: list[ContextDocument]) -> str:
    if not documents:
        return (
            "Aucun document de contexte n'a encore été fourni. "
            "Produis un contenu générique pour une académie de langues, "
            "puis recommande d'ajouter des fichiers Markdown dans content/academy_context/."
        )
    sections = []
    for document in documents:
        sections.append(f"# {document.title}\n\n{document.content}")
    return "\n\n---\n\n".join(sections)
