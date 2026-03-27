from __future__ import annotations

from typing import Any

import httpx

from .auth import RequestAuth
from .config import ClientConfig
from .http_client import AsertuHttpClient
from .resources import EventsResource, PricingResource, TenantsResource


class AsertuOptimizerClient:
    def __init__(
        self,
        *,
        base_url: str = "https://api.dev.asertu.ai",
        admin_api_key: str | None = None,
        tenant_api_key: str | None = None,
        bearer_token: str | None = None,
        tenant_id: str | None = None,
        timeout: float = 10.0,
        max_retries: int = 2,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.config = ClientConfig(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.auth = RequestAuth(
            admin_api_key=admin_api_key,
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
        self.pricing = PricingResource(self._http_client)
        self.events = EventsResource(self._http_client)

    def close(self) -> None:
        self._http_client.close()

    def __enter__(self) -> AsertuOptimizerClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
