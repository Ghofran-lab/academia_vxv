from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from urllib.parse import urljoin

from .models import Exercise

CORRECTION_MARKERS = re.compile(r"\b(correction|corrig[ée]s?|r[ée]ponses?|solution)\b", re.I)
QUESTION_MARKERS = re.compile(r"(__+|\.\.\.+|\[\s*\]|_{2,})")
NOISE_TAGS = {"script", "style", "noscript", "iframe", "nav", "header", "footer", "form"}
BLOCK_TAGS = {"p", "div", "li", "br", "tr", "h1", "h2", "h3", "h4", "main", "article", "section"}


class _ExerciseHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.heading_parts: list[str] = []
        self.text_parts: list[str] = []
        self.question_candidates: list[str] = []
        self.links: list[str] = []
        self._tag_stack: list[str] = []
        self._skip_depth = 0
        self._capture_title = False
        self._capture_heading = False
        self._current_block: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self._tag_stack.append(tag)
        attrs_dict = dict(attrs)
        if tag in NOISE_TAGS:
            self._skip_depth += 1
        if self._skip_depth:
            return
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"] or "")
        if tag == "title":
            self._capture_title = True
        if tag == "h1":
            self._capture_heading = True
        if tag in BLOCK_TAGS:
            self._flush_block()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._skip_depth and tag in NOISE_TAGS:
            self._skip_depth -= 1
        if self._skip_depth:
            return
        if tag == "title":
            self._capture_title = False
        if tag == "h1":
            self._capture_heading = False
        if tag in BLOCK_TAGS:
            self._flush_block()
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = _normalize_space(data)
        if not text:
            return
        if self._capture_title:
            self.title_parts.append(text)
        if self._capture_heading:
            self.heading_parts.append(text)
        self._current_block.append(text)

    def close(self) -> None:
        self._flush_block()
        super().close()

    def _flush_block(self) -> None:
        text = _normalize_space(" ".join(self._current_block))
        self._current_block = []
        if not text:
            return
        self.text_parts.append(text)
        if "?" in text or QUESTION_MARKERS.search(text):
            self.question_candidates.append(text)


def parse_exercise(html_text: str, source_url: str) -> Exercise:
    parsed = _parse(html_text)
    title = _first_non_empty(parsed.heading_parts, parsed.title_parts, ["Exercice français"])
    lines = _dedupe(parsed.text_parts)
    statement_lines, correction_lines = _split_correction(lines)
    questions = _dedupe(parsed.question_candidates)

    return Exercise(
        source_url=source_url,
        title=title,
        statement="\n".join(statement_lines).strip(),
        questions=questions,
        correction="\n".join(correction_lines).strip() or None,
        metadata={"domain": "francaisfacile.com"},
    )


def discover_exercise_links(html_text: str, base_url: str) -> list[str]:
    parsed = _parse(html_text)
    links: list[str] = []
    seen: set[str] = set()
    for href in parsed.links:
        url = urljoin(base_url, html.unescape(href))
        if "francaisfacile.com" not in url:
            continue
        if not _looks_like_exercise_url(url):
            continue
        normalized = url.split("#", 1)[0]
        if normalized not in seen:
            seen.add(normalized)
            links.append(normalized)
    return links


def _parse(html_text: str) -> _ExerciseHTMLParser:
    parser = _ExerciseHTMLParser()
    parser.feed(html_text)
    parser.close()
    return parser


def _looks_like_exercise_url(url: str) -> bool:
    lowered = url.lower()
    return "exercice" in lowered and lowered.endswith((".php", ".html", "/"))


def _normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _split_correction(lines: list[str]) -> tuple[list[str], list[str]]:
    for index, line in enumerate(lines):
        if CORRECTION_MARKERS.search(line):
            return lines[:index], lines[index:]
    return lines, []


def _first_non_empty(*groups: list[str]) -> str:
    for group in groups:
        for value in group:
            cleaned = _normalize_space(value)
            if cleaned:
                return cleaned
    return "Exercice français"


def _dedupe(values) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
