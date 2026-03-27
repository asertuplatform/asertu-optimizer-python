from __future__ import annotations

import os

import httpx

from .async_http_client import AsyncAsertuHttpClient
from .async_resources import (
    AsyncAnalyticsResource,
    AsyncBillingResource,
    AsyncEventsResource,
    AsyncHistoryResource,
    AsyncSettingsResource,
    AsyncTenantsResource,
)
from .auth import RequestAuth
from .config import ClientConfig
from .telemetry import TelemetryHandler


class AsyncAsertuOptimizerClient:
    @classmethod
    def from_env(cls) -> AsyncAsertuOptimizerClient:
        return cls(
            base_url=os.getenv("ASERTU_BASE_URL", "https://api.dev.asertu.ai"),
            tenant_api_key=os.getenv("ASERTU_TENANT_API_KEY"),
            bearer_token=os.getenv("ASERTU_BEARER_TOKEN"),
            tenant_id=os.getenv("ASERTU_TENANT_ID"),
        )

    def __init__(
        self,
        *,
        base_url: str = "https://api.dev.asertu.ai",
        tenant_api_key: str | None = None,
        bearer_token: str | None = None,
        tenant_id: str | None = None,
        timeout: float = 10.0,
        max_retries: int = 2,
        telemetry_handler: TelemetryHandler | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.config = ClientConfig(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            telemetry_handler=telemetry_handler,
        )
        self.auth = RequestAuth(
            tenant_api_key=tenant_api_key,
            bearer_token=bearer_token,
            tenant_id=tenant_id,
        )
        self._http_client = AsyncAsertuHttpClient(
            config=self.config,
            auth=self.auth,
            client=http_client,
        )

        self.tenants = AsyncTenantsResource(self._http_client)
        self.events = AsyncEventsResource(self._http_client)
        self.analytics = AsyncAnalyticsResource(self._http_client)
        self.history = AsyncHistoryResource(self._http_client)
        self.billing = AsyncBillingResource(self._http_client)
        self.settings = AsyncSettingsResource(self._http_client)

    async def aclose(self) -> None:
        await self._http_client.aclose()

    async def __aenter__(self) -> AsyncAsertuOptimizerClient:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()
