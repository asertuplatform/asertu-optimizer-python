from __future__ import annotations

import json

import httpx
import pytest

from asertu_optimizer import (
    AsertuOptimizerClient,
    AuthenticationError,
    ContractUnavailableError,
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
