from __future__ import annotations


class Optimizer:
    """Example client for the asertu Optimizer SDK."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def optimize(self, text: str) -> dict:
        return {
            "optimized": False,
            "input": text,
            "message": "Placeholder SDK package to reserve the PyPI name.",
        }
