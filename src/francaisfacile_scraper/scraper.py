from __future__ import annotations

import time
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

from .models import Exercise
from .parser import discover_exercise_links, parse_exercise

DEFAULT_USER_AGENT = "academia-vxv-knowledge-base-bot/0.1 (+contact: owner@example.com)"


class ScrapingBlockedError(RuntimeError):
    """Levée quand robots.txt ou le domaine empêchent une requête."""


@dataclass(slots=True)
class ScraperConfig:
    user_agent: str = DEFAULT_USER_AGENT
    delay_seconds: float = 2.0
    timeout_seconds: float = 20.0
    respect_robots: bool = True
    max_pages: int = 50


class FrancaisFacileScraper:
    """Client HTTP sobre et poli pour exporter uniquement des pages publiques."""

    def __init__(self, config: ScraperConfig | None = None) -> None:
        self.config = config or ScraperConfig()
        self._robots: dict[str, RobotFileParser] = {}
        self._last_request_at = 0.0

    def scrape_url(self, url: str) -> Exercise:
        html = self.fetch(url)
        return parse_exercise(html, url)

    def discover_from_index(self, url: str) -> list[str]:
        html = self.fetch(url)
        return discover_exercise_links(html, url)[: self.config.max_pages]

    def fetch(self, url: str) -> str:
        self._validate_domain(url)
        if self.config.respect_robots and not self._can_fetch(url):
            raise ScrapingBlockedError(f"robots.txt interdit l'accès à {url}")
        self._throttle()
        request = Request(url, headers={"User-Agent": self.config.user_agent})
        with urlopen(request, timeout=self.config.timeout_seconds) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")

    def _validate_domain(self, url: str) -> None:
        hostname = urlparse(url).hostname or ""
        if not hostname.endswith("francaisfacile.com"):
            raise ValueError(f"Domaine non autorisé: {hostname}")

    def _can_fetch(self, url: str) -> bool:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        parser = self._robots.get(base)
        if parser is None:
            parser = RobotFileParser()
            parser.set_url(f"{base}/robots.txt")
            parser.read()
            self._robots[base] = parser
        return parser.can_fetch(self.config.user_agent, url)

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        wait_for = self.config.delay_seconds - elapsed
        if wait_for > 0:
            time.sleep(wait_for)
        self._last_request_at = time.monotonic()
