from __future__ import annotations

from ..exceptions import ContractUnavailableError
from ..models.tenants import TenantCreateRequest, TenantCreateResult, TenantList
from .base import BaseResource


class TenantsResource(BaseResource):
    def list(
        self,
        *,
        bearer_token: str | None = None,
    ) -> TenantList:
        data = self.http_client.request(
            "GET",
            "/v1/tenants",
            auth=self.build_auth(bearer_token=bearer_token),
        )
        return TenantList.from_dict(dict(data))

    def create(
        self,
        *,
        name: str,
        plan: str,
        external_id: str | None = None,
        metadata: dict[str, object] | None = None,
        admin_api_key: str | None = None,
    ) -> TenantCreateResult:
        _ = admin_api_key
        _ = TenantCreateRequest(
            name=name,
            plan=plan,
            external_id=external_id,
            metadata=metadata or {},
        )
        raise ContractUnavailableError(
            "Tenant creation is part of the SDK surface, but the admin endpoint "
            "is not published in the current OpenAPI contract yet."
        )
