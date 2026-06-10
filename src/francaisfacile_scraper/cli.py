from __future__ import annotations

import argparse
from pathlib import Path

from .markdown import write_markdown
from .scraper import DEFAULT_USER_AGENT, FrancaisFacileScraper, ScraperConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape des exercices publics francaisfacile.com et les exporte en Markdown."
    )
    parser.add_argument("--url", action="append", default=[], help="URL d'exercice à exporter; option répétable.")
    parser.add_argument("--urls-file", type=Path, help="Fichier texte contenant une URL par ligne.")
    parser.add_argument("--index-url", action="append", default=[], help="Page d'index où découvrir des liens d'exercices.")
    parser.add_argument("--output-dir", type=Path, default=Path("knowledge_base/francaisfacile"))
    parser.add_argument("--max-pages", type=int, default=50)
    parser.add_argument("--delay", type=float, default=2.0, help="Pause en secondes entre deux requêtes.")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument(
        "--ignore-robots",
        action="store_true",
        help="Désactive la vérification robots.txt. À éviter sans autorisation explicite.",
    )
    return parser


def collect_urls(args: argparse.Namespace, scraper: FrancaisFacileScraper) -> list[str]:
    urls = list(args.url)
    if args.urls_file:
        urls.extend(
            line.strip()
            for line in args.urls_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
    for index_url in args.index_url:
        urls.extend(scraper.discover_from_index(index_url))
    return list(dict.fromkeys(urls))[: args.max_pages]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = ScraperConfig(
        user_agent=args.user_agent,
        delay_seconds=args.delay,
        respect_robots=not args.ignore_robots,
        max_pages=args.max_pages,
    )
    scraper = FrancaisFacileScraper(config)
    urls = collect_urls(args, scraper)
    if not urls:
        parser.error("Indiquez au moins --url, --urls-file ou --index-url.")

    for url in urls:
        exercise = scraper.scrape_url(url)
        path = write_markdown(exercise, args.output_dir)
        print(f"Exporté: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
