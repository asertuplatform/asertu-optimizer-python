from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from ..instrumentation import extract_provider_usage
from ..models.events import EventIngestionRequest, EventIngestionResponse
from .base import AsyncBaseResource


class AsyncEventsResource(AsyncBaseResource):
    async def ingest(
        self,
        event: EventIngestionRequest,
        *,
        tenant_api_key: str | None = None,
    ) -> EventIngestionResponse:
        auth = self.build_auth(tenant_api_key=tenant_api_key)
        self.require_tenant_api_key(self.http_client.default_auth.merged_with(auth))
        data = await self.http_client.request(
            "POST",
            "/v1/events",
            json_body=event.to_payload(),
            auth=auth,
        )
        return EventIngestionResponse.from_dict(dict(data))

    async def track_llm_call(
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
        return await self.ingest(event, tenant_api_key=tenant_api_key)

    async def track_openai_call(self, **kwargs: Any) -> EventIngestionResponse:
        return await self.track_llm_call(provider="openai", **kwargs)

    async def track_anthropic_call(self, **kwargs: Any) -> EventIngestionResponse:
        return await self.track_llm_call(provider="anthropic", **kwargs)

    async def track_bedrock_call(self, **kwargs: Any) -> EventIngestionResponse:
        return await self.track_llm_call(provider="bedrock", **kwargs)

    async def track_provider_response(
        self,
        *,
        provider: str,
        feature: str,
        response: Any,
        status: str,
        model: str | None = None,
        tenant_api_key: str | None = None,
        request_id: str | None = None,
        user_id: str | None = None,
        timestamp: datetime | None = None,
        metadata: dict[str, Any] | None = None,
        cost: float | None = None,
        event_type: str = "llm_request",
    ) -> EventIngestionResponse:
        usage = extract_provider_usage(provider, response, model=model)
        return await self.track_llm_call(
            provider=usage.provider,
            model=usage.model or model or "unknown",
            feature=feature,
            status=status,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
            cost=cost or usage.cost,
            request_id=request_id,
            user_id=user_id,
            timestamp=timestamp,
            metadata=metadata,
            tenant_api_key=tenant_api_key,
            event_type=event_type,
        )

    async def track_openai_response(self, **kwargs: Any) -> EventIngestionResponse:
        return await self.track_provider_response(provider="openai", **kwargs)

    async def track_anthropic_response(self, **kwargs: Any) -> EventIngestionResponse:
        return await self.track_provider_response(provider="anthropic", **kwargs)

    async def track_bedrock_response(self, **kwargs: Any) -> EventIngestionResponse:
        return await self.track_provider_response(provider="bedrock", **kwargs)
