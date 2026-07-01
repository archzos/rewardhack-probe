"""Model adapters for probe execution."""

from __future__ import annotations

from typing import Protocol


class ModelAdapter(Protocol):
    """Common interface for probe subjects."""

    model_name: str

    def complete(self, prompt: str, *, system: str | None = None, temperature: float = 0.0) -> str:
        ...
