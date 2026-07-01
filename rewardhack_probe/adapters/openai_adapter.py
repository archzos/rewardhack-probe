"""OpenAI API adapter for probe execution."""

from __future__ import annotations

import os


class OpenAIAdapter:
    """Minimal chat-completions adapter backed by the OpenAI HTTP API."""

    def __init__(self, model_name: str | None = None, api_key: str | None = None) -> None:
        self.model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-4o")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def complete(self, prompt: str, *, system: str | None = None, temperature: float = 0.0) -> str:
        if not self.api_key:
            raise NotImplementedError("OPENAI_API_KEY is not configured")
        try:
            import requests
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("requests dependency missing") from exc
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system or "You are a careful assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
