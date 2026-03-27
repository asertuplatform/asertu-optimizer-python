from __future__ import annotations

import os
from typing import Any

import httpx

from .auth import RequestAuth
from .config import DEFAULT_BASE_URL, ClientConfig
from .http_client import AsertuHttpClient
from .resources import (
    AnalyticsResource,
    BillingResource,
    EventsResource,
    HistoryResource,
    SettingsResource,
    TenantsResource,
)
from .telemetry import TelemetryHandler


class AsertuOptimizerClient:
    @classmethod
    def from_env(cls) -> AsertuOptimizerClient:
        return cls(
            base_url=os.getenv("ASERTU_BASE_URL", DEFAULT_BASE_URL),
            tenant_api_key=os.getenv("ASERTU_TENANT_API_KEY"),
            bearer_token=os.getenv("ASERTU_BEARER_TOKEN"),
            tenant_id=os.getenv("ASERTU_TENANT_ID"),
        )

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        tenant_api_key: str | None = None,
        bearer_token: str | None = None,
        tenant_id: str | None = None,
        timeout: float = 10.0,
        max_retries: int = 2,
        telemetry_handler: TelemetryHandler | None = None,
        http_client: httpx.Client | None = None,
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
        self._http_client = AsertuHttpClient(
            config=self.config,
            auth=self.auth,
            client=http_client,
        )

        self.tenants = TenantsResource(self._http_client)
        self.events = EventsResource(self._http_client)
        self.analytics = AnalyticsResource(self._http_client)
        self.history = HistoryResource(self._http_client)
        self.billing = BillingResource(self._http_client)
        self.settings = SettingsResource(self._http_client)

    def close(self) -> None:
        self._http_client.close()

    def __enter__(self) -> AsertuOptimizerClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
