from pathlib import Path

from academia_content.context import load_context_documents, render_context
from academia_content.generator import build_weekly_prompt, save_generated_content
from academia_content.telegram import chunk_message


def test_load_context_documents_reads_markdown_files_sorted(tmp_path: Path):
    (tmp_path / "vision.md").write_text("Vision future", encoding="utf-8")
    (tmp_path / "mission.md").write_text("Mission actuelle", encoding="utf-8")
    (tmp_path / "empty.md").write_text("   ", encoding="utf-8")
    (tmp_path / "README.md").write_text("Documentation", encoding="utf-8")
    (tmp_path / "mission.example.md").write_text("Exemple", encoding="utf-8")

    documents = load_context_documents(tmp_path)

    assert [document.path.name for document in documents] == ["mission.md", "vision.md"]
    assert render_context(documents).startswith("# Mission")
    assert "Mission actuelle" in render_context(documents)


def test_build_weekly_prompt_includes_academy_context(tmp_path: Path):
    (tmp_path / "mission.md").write_text("Aider les élèves à parler anglais avec confiance.", encoding="utf-8")

    prompt = build_weekly_prompt(tmp_path)

    assert "Aider les élèves" in prompt
    assert "5 contenus prêts à poster" in prompt
    assert "test de niveau" in prompt


def test_save_generated_content_creates_markdown_file(tmp_path: Path):
    path = save_generated_content("# Planning\n\nContenu", tmp_path)

    assert path.parent == tmp_path
    assert path.suffix == ".md"
    assert path.read_text(encoding="utf-8") == "# Planning\n\nContenu\n"


def test_chunk_message_splits_long_text_on_newline():
    text = "Intro\n" + "a" * 20 + "\nSuite"

    chunks = chunk_message(text, limit=15)

    assert len(chunks) > 1
    assert all(len(chunk) <= 20 for chunk in chunks)
