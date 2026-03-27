from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

JsonDict = dict[str, Any]


def _datetime_to_iso8601(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


@dataclass(frozen=True, slots=True)
class EventIngestionRequest:
    provider: str
    model: str
    feature: str
    status: str
    schema_version: str = "1.0"
    event_type: str = "llm_request"
    request_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime | None = None
    user_id: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None
    metadata: JsonDict = field(default_factory=dict)

    def to_payload(self) -> JsonDict:
        total_tokens = self.total_tokens
        if total_tokens is None and None not in (self.prompt_tokens, self.completion_tokens):
            total_tokens = (self.prompt_tokens or 0) + (self.completion_tokens or 0)

        payload: JsonDict = {
            "schema_version": self.schema_version,
            "event_type": self.event_type,
            "request_id": self.request_id,
            "provider": self.provider,
            "model": self.model,
            "feature": self.feature,
            "status": self.status,
            "timestamp": _datetime_to_iso8601(self.timestamp),
            "user_id": self.user_id,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": total_tokens,
            "cost": self.cost,
            "metadata": self.metadata,
        }
        return {key: value for key, value in payload.items() if value is not None}


@dataclass(frozen=True, slots=True)
class EventIngestionResponse:
    message: str | None = None
    tenant_id: str | None = None
    s3_key: str | None = None
    timestamp: str | None = None
    ingested_at: str | None = None
    ingestion_date: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> EventIngestionResponse:
        return cls(
            message=data.get("message"),
            tenant_id=data.get("tenant_id"),
            s3_key=data.get("s3_key"),
            timestamp=data.get("timestamp"),
            ingested_at=data.get("ingested_at"),
            ingestion_date=data.get("ingestion_date"),
        )
