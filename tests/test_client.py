from __future__ import annotations

import asyncio
import json

import httpx
import pytest

from asertu_optimizer import (
    AsertuOptimizerClient,
    AsyncAsertuOptimizerClient,
    AuthenticationError,
    ContractUnavailableError,
    MissingCredentialsError,
    ValidationError,
)
from asertu_optimizer.models import PricingRule


def test_events_track_llm_call_sends_pythonic_payload() -> None:
    captured_headers: dict[str, str] = {}
    captured_path = ""
    captured_body: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_headers, captured_path, captured_body
        captured_headers = dict(request.headers)
        captured_path = request.url.path
        captured_body = json.loads(request.content.decode())
        return httpx.Response(
            200,
            json={
                "message": "accepted",
                "tenant_id": "tenant-123",
                "s3_key": "events/1.json",
            },
        )

    client = AsertuOptimizerClient(
        tenant_api_key="tenant-key",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    response = client.events.track_llm_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="support_chat",
        input_tokens=1200,
        output_tokens=800,
        status="success",
        metadata={"env": "test"},
    )

    assert captured_path == "/v1/events"
    assert captured_headers["x-api-key"] == "tenant-key"
    assert captured_body["provider"] == "openai"
    assert captured_body["prompt_tokens"] == 1200
    assert captured_body["completion_tokens"] == 800
    assert captured_body["total_tokens"] == 2000
    assert response.tenant_id == "tenant-123"


def test_track_openai_call_sets_provider_implicitly() -> None:
    captured_body: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_body
        captured_body = json.loads(request.content.decode())
        return httpx.Response(200, json={"message": "accepted"})

    client = AsertuOptimizerClient(
        tenant_api_key="tenant-key",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    client.events.track_openai_call(
        model="gpt-4.1-mini",
        feature="assistant",
        input_tokens=10,
        output_tokens=20,
        status="success",
    )

    assert captured_body["provider"] == "openai"


def test_tenants_list_uses_bearer_auth() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer jwt-token"
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "tenant_id": "tenant-1",
                        "name": "Acme",
                        "role": "owner",
                        "plan": "free",
                        "is_default": True,
                    }
                ]
            },
        )

    client = AsertuOptimizerClient(
        bearer_token="jwt-token",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = client.tenants.list()

    assert len(result.items) == 1
    assert result.items[0].name == "Acme"


def test_auth_override_per_call() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer override-token"
        return httpx.Response(200, json={"items": []})

    client = AsertuOptimizerClient(
        bearer_token="default-token",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = client.tenants.list(bearer_token="override-token")

    assert result.items == []


def test_raises_authentication_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "invalid token"})

    client = AsertuOptimizerClient(
        bearer_token="bad-token",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    with pytest.raises(AuthenticationError):
        client.tenants.list()


def test_admin_resources_fail_closed_until_contract_exists() -> None:
    client = AsertuOptimizerClient(admin_api_key="admin-key")

    with pytest.raises(ContractUnavailableError):
        client.tenants.create(name="Acme", plan="free")

    with pytest.raises(ContractUnavailableError):
        client.pricing.upsert(PricingRule(provider="openai", model="gpt-4.1-mini"))


def test_requires_bearer_token_for_tenants_list() -> None:
    client = AsertuOptimizerClient()

    with pytest.raises(MissingCredentialsError):
        client.tenants.list()


def test_requires_tenant_scope_for_analytics_reads() -> None:
    client = AsertuOptimizerClient(bearer_token="jwt-token")

    with pytest.raises(MissingCredentialsError):
        client.analytics.dashboard_summary(preset="today")


def test_dashboard_summary_sends_tenant_headers_and_query() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer jwt-token"
        assert request.headers["X-Tenant-Id"] == "tenant-123"
        assert request.url.path == "/v1/dashboard/summary"
        assert request.url.params["preset"] == "today"
        return httpx.Response(
            200,
            json={
                "tenant_id": "tenant-123",
                "from": "2026-03-27",
                "to": "2026-03-27",
                "total_requests": 42,
                "total_tokens": 24000,
                "total_cost": 12.5,
                "total_errors": 1,
            },
        )

    client = AsertuOptimizerClient(
        bearer_token="jwt-token",
        tenant_id="tenant-123",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = client.analytics.dashboard_summary(preset="today")

    assert result.total_requests == 42
    assert result.total_cost == 12.5


def test_history_daily_cost_maps_time_series() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer jwt-token"
        assert request.headers["X-Tenant-Id"] == "tenant-123"
        assert request.url.path == "/v1/history/daily-cost"
        assert request.url.params["granularity"] == "daily"
        return httpx.Response(
            200,
            json={
                "tenant_id": "tenant-123",
                "granularity": "daily",
                "points": [
                    {"bucket": "2026-03-26", "value": 3.1},
                    {"bucket": "2026-03-27", "value": 4.2},
                ],
            },
        )

    client = AsertuOptimizerClient(
        bearer_token="jwt-token",
        tenant_id="tenant-123",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = client.history.daily_cost(preset="last_7_days", granularity="daily")

    assert result.granularity == "daily"
    assert len(result.points) == 2
    assert result.points[1].value == 4.2


def test_usage_by_model_supports_per_call_override() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer override-jwt"
        assert request.headers["X-Tenant-Id"] == "tenant-999"
        assert request.url.path == "/v1/usage/by-model"
        return httpx.Response(
            200,
            json={
                "tenant_id": "tenant-999",
                "from": "2026-03-20",
                "to": "2026-03-27",
                "items": [
                    {
                        "key": "gpt-4.1-mini",
                        "label": "gpt-4.1-mini",
                        "requests": 10,
                        "tokens": 2000,
                        "cost": 1.4,
                        "errors": 0,
                    }
                ],
            },
        )

    client = AsertuOptimizerClient(
        bearer_token="default-jwt",
        tenant_id="tenant-123",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = client.analytics.usage_by_model(
        bearer_token="override-jwt",
        tenant_id="tenant-999",
        preset="last_7_days",
    )

    assert result.items[0].key == "gpt-4.1-mini"


def test_date_range_validation_rejects_preset_and_explicit_dates() -> None:
    client = AsertuOptimizerClient(bearer_token="jwt-token", tenant_id="tenant-123")

    with pytest.raises(ValidationError):
        client.analytics.dashboard_summary(
            preset="today",
            from_date="2026-03-01",
            to_date="2026-03-27",
        )


def test_granularity_validation_rejects_unknown_values() -> None:
    client = AsertuOptimizerClient(bearer_token="jwt-token", tenant_id="tenant-123")

    with pytest.raises(ValidationError):
        client.history.daily_cost(preset="last_7_days", granularity="weekly")


def test_event_validation_rejects_inconsistent_token_counts() -> None:
    client = AsertuOptimizerClient(tenant_api_key="tenant-key")

    with pytest.raises(ValidationError):
        client.events.track_llm_call(
            provider="openai",
            model="gpt-4.1-mini",
            feature="assistant",
            input_tokens=10,
            output_tokens=20,
            total_tokens=50,
            status="success",
        )


def test_from_env_builds_client(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ASERTU_BASE_URL", "https://api.dev.asertu.ai")
    monkeypatch.setenv("ASERTU_TENANT_API_KEY", "tenant-key")
    monkeypatch.setenv("ASERTU_BEARER_TOKEN", "jwt-token")
    monkeypatch.setenv("ASERTU_TENANT_ID", "tenant-123")

    client = AsertuOptimizerClient.from_env()

    assert client.config.base_url == "https://api.dev.asertu.ai"
    assert client.auth.tenant_api_key == "tenant-key"
    assert client.auth.bearer_token == "jwt-token"
    assert client.auth.tenant_id == "tenant-123"


def test_track_openai_response_extracts_usage() -> None:
    captured_body: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_body
        captured_body = json.loads(request.content.decode())
        return httpx.Response(200, json={"message": "accepted"})

    client = AsertuOptimizerClient(
        tenant_api_key="tenant-key",
        http_client=httpx.Client(
            base_url="https://api.dev.asertu.ai",
            transport=httpx.MockTransport(handler),
        ),
    )

    client.events.track_openai_response(
        feature="support_chat",
        status="success",
        response={
            "model": "gpt-4.1-mini",
            "usage": {
                "prompt_tokens": 111,
                "completion_tokens": 222,
                "total_tokens": 333,
            },
        },
    )

    assert captured_body["provider"] == "openai"
    assert captured_body["prompt_tokens"] == 111
    assert captured_body["completion_tokens"] == 222
    assert captured_body["total_tokens"] == 333


def test_async_events_track_llm_call() -> None:
    async def run() -> None:
        captured_body: dict[str, object] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal captured_body
            captured_body = json.loads(request.content.decode())
            return httpx.Response(200, json={"message": "accepted", "tenant_id": "tenant-1"})

        client = AsyncAsertuOptimizerClient(
            tenant_api_key="tenant-key",
            http_client=httpx.AsyncClient(
                base_url="https://api.dev.asertu.ai",
                transport=httpx.MockTransport(handler),
            ),
        )
        try:
            result = await client.events.track_openai_call(
                model="gpt-4.1-mini",
                feature="async_chat",
                input_tokens=12,
                output_tokens=34,
                status="success",
            )
        finally:
            await client.aclose()

        assert result.tenant_id == "tenant-1"
        assert captured_body["provider"] == "openai"
        assert captured_body["total_tokens"] == 46

    asyncio.run(run())


def test_async_dashboard_summary() -> None:
    async def run() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.headers["Authorization"] == "Bearer jwt-token"
            assert request.headers["X-Tenant-Id"] == "tenant-123"
            return httpx.Response(
                200,
                json={
                    "tenant_id": "tenant-123",
                    "from": "2026-03-27",
                    "to": "2026-03-27",
                    "total_requests": 7,
                    "total_tokens": 700,
                    "total_cost": 1.23,
                    "total_errors": 0,
                },
            )

        client = AsyncAsertuOptimizerClient(
            bearer_token="jwt-token",
            tenant_id="tenant-123",
            http_client=httpx.AsyncClient(
                base_url="https://api.dev.asertu.ai",
                transport=httpx.MockTransport(handler),
            ),
        )
        try:
            result = await client.analytics.dashboard_summary(preset="today")
        finally:
            await client.aclose()

        assert result.total_requests == 7
        assert result.total_cost == 1.23

    asyncio.run(run())
