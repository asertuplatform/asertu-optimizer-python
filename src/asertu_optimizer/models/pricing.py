from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass(frozen=True, slots=True)
class PricingRule:
    provider: str
    model: str
    input_cost_per_1k_tokens: float | None = None
    output_cost_per_1k_tokens: float | None = None
    currency: str = "USD"
    metadata: JsonDict = field(default_factory=dict)

    def to_payload(self) -> JsonDict:
        return {
            "provider": self.provider,
            "model": self.model,
            "input_cost_per_1k_tokens": self.input_cost_per_1k_tokens,
            "output_cost_per_1k_tokens": self.output_cost_per_1k_tokens,
            "currency": self.currency,
            "metadata": self.metadata,
        }
