from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class SdkTelemetryEvent:
    method: str
    path: str
    status_code: int | None
    duration_ms: float
    success: bool
    error_type: str | None = None
    request_id: str | None = None
    timestamp: float = field(default_factory=time)


class TelemetryHandler(Protocol):
    def __call__(self, event: SdkTelemetryEvent) -> Any:
        ...


class InMemoryTelemetryCollector:
    def __init__(self) -> None:
        self.events: list[SdkTelemetryEvent] = []

    def __call__(self, event: SdkTelemetryEvent) -> None:
        self.events.append(event)
