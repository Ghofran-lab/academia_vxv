from __future__ import annotations

import argparse
from pathlib import Path

from .generator import build_weekly_prompt, generate_weekly_content, save_generated_content
from .telegram import send_message


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Génère et livre les contenus social media de l'académie.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    weekly = subparsers.add_parser("weekly", help="Génère le planning de contenus hebdomadaire.")
    weekly.add_argument("--context-dir", type=Path, default=Path("content/academy_context"))
    weekly.add_argument("--output-dir", type=Path, default=Path("content/generated"))
    weekly.add_argument("--send-telegram", action="store_true", help="Envoie le résultat sur Telegram.")
    weekly.add_argument("--dry-run", action="store_true", help="Affiche le prompt sans appeler l'IA.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "weekly":
        if args.dry_run:
            print(build_weekly_prompt(args.context_dir))
            return 0
        content = generate_weekly_content(args.context_dir)
        path = save_generated_content(content, args.output_dir)
        print(f"Contenu généré: {path}")
        if args.send_telegram:
            send_message(f"🎓 Contenus de la semaine\n\n{content}")
            print("Contenu envoyé sur Telegram")
        return 0

    parser.error("Commande inconnue")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
