from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from ..models.events import EventIngestionRequest, EventIngestionResponse
from .base import BaseResource


class EventsResource(BaseResource):
    def ingest(
        self,
        event: EventIngestionRequest,
        *,
        tenant_api_key: str | None = None,
    ) -> EventIngestionResponse:
        auth = self.build_auth(tenant_api_key=tenant_api_key)
        self.require_tenant_api_key(self.http_client.default_auth.merged_with(auth))
        payload = event.to_payload()
        data = self.http_client.request(
            "POST",
            "/v1/events",
            json_body=payload,
            auth=auth,
        )
        return EventIngestionResponse.from_dict(dict(data))

    def track_llm_call(
        self,
        *,
        provider: str,
        model: str,
        feature: str,
        status: str,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        total_tokens: int | None = None,
        cost: float | None = None,
        request_id: str | None = None,
        user_id: str | None = None,
        timestamp: datetime | None = None,
        metadata: dict[str, Any] | None = None,
        tenant_api_key: str | None = None,
        event_type: str = "llm_request",
    ) -> EventIngestionResponse:
        event = EventIngestionRequest(
            provider=provider,
            model=model,
            feature=feature,
            status=status,
            event_type=event_type,
            request_id=request_id or str(uuid4()),
            timestamp=timestamp,
            user_id=user_id,
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            total_tokens=total_tokens,
            cost=cost,
            metadata=metadata or {},
        )
        return self.ingest(event, tenant_api_key=tenant_api_key)

    def track_openai_call(self, **kwargs: Any) -> EventIngestionResponse:
        return self.track_llm_call(provider="openai", **kwargs)

    def track_anthropic_call(self, **kwargs: Any) -> EventIngestionResponse:
        return self.track_llm_call(provider="anthropic", **kwargs)

    def track_bedrock_call(self, **kwargs: Any) -> EventIngestionResponse:
        return self.track_llm_call(provider="bedrock", **kwargs)
