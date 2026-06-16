from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-4.1-mini"


class OpenAIConfigError(RuntimeError):
    pass


class OpenAIRequestError(RuntimeError):
    pass


def generate_text(prompt: str, system_prompt: str, model: str | None = None, api_key: str | None = None) -> str:
    """Génère du texte via l'API Responses sans dépendance externe."""
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_api_key:
        raise OpenAIConfigError("La variable d'environnement OPENAI_API_KEY est requise.")

    payload = {
        "model": model or os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {resolved_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise OpenAIRequestError(f"Erreur OpenAI HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise OpenAIRequestError(f"Erreur réseau OpenAI: {exc}") from exc

    text = data.get("output_text")
    if isinstance(text, str) and text.strip():
        return text.strip()

    # Fallback robuste pour les réponses structurées.
    chunks: list[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                chunks.append(content["text"])
    if chunks:
        return "\n".join(chunks).strip()
    raise OpenAIRequestError("Réponse OpenAI sans texte exploitable.")
