from __future__ import annotations

from dataclasses import dataclass

from ..auth import RequestAuth
from ..http_client import AsertuHttpClient


@dataclass(slots=True)
class BaseResource:
    http_client: AsertuHttpClient

    @staticmethod
    def build_auth(
        *,
        admin_api_key: str | None = None,
        tenant_api_key: str | None = None,
        bearer_token: str | None = None,
        tenant_id: str | None = None,
    ) -> RequestAuth | None:
        if not any((admin_api_key, tenant_api_key, bearer_token, tenant_id)):
            return None
        return RequestAuth(
            admin_api_key=admin_api_key,
            tenant_api_key=tenant_api_key,
            bearer_token=bearer_token,
            tenant_id=tenant_id,
        )
