from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request


MAX_TELEGRAM_TEXT = 3900


class TelegramConfigError(RuntimeError):
    pass


class TelegramRequestError(RuntimeError):
    pass


def chunk_message(text: str, limit: int = MAX_TELEGRAM_TEXT) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks: list[str] = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        chunks.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()
    if remaining:
        chunks.append(remaining)
    return chunks


def send_message(text: str, bot_token: str | None = None, chat_id: str | None = None) -> None:
    resolved_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
    resolved_chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not resolved_token or not resolved_chat_id:
        raise TelegramConfigError("TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID sont requis.")

    url = f"https://api.telegram.org/bot{resolved_token}/sendMessage"
    for chunk in chunk_message(text):
        payload = urllib.parse.urlencode({"chat_id": resolved_chat_id, "text": chunk}).encode("utf-8")
        request = urllib.request.Request(url, data=payload, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise TelegramRequestError(f"Erreur Telegram HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise TelegramRequestError(f"Erreur réseau Telegram: {exc}") from exc
        if not data.get("ok"):
            raise TelegramRequestError(f"Réponse Telegram inattendue: {data}")
