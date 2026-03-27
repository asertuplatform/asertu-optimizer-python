from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestAuth:
    admin_api_key: str | None = None
    tenant_api_key: str | None = None
    bearer_token: str | None = None
    tenant_id: str | None = None

    def merged_with(self, override: RequestAuth | None) -> RequestAuth:
        if override is None:
            return self
        return RequestAuth(
            admin_api_key=override.admin_api_key or self.admin_api_key,
            tenant_api_key=override.tenant_api_key or self.tenant_api_key,
            bearer_token=override.bearer_token or self.bearer_token,
            tenant_id=override.tenant_id or self.tenant_id,
        )

    def headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        api_key = self.tenant_api_key or self.admin_api_key
        if api_key:
            headers["x-api-key"] = api_key
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        if self.tenant_id:
            headers["X-Tenant-Id"] = self.tenant_id
        return headers

    @property
    def has_api_key(self) -> bool:
        return bool(self.tenant_api_key or self.admin_api_key)

    @property
    def has_bearer_token(self) -> bool:
        return bool(self.bearer_token)
