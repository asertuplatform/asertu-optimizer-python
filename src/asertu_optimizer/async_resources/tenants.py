from __future__ import annotations

from collections.abc import AsyncIterator

from ..exceptions import ContractUnavailableError, ValidationError
from ..models.tenants import Tenant, TenantCreateRequest, TenantCreateResult, TenantList
from .base import AsyncBaseResource


class AsyncTenantsResource(AsyncBaseResource):
    async def list(
        self,
        *,
        bearer_token: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> TenantList:
        auth = self.build_auth(bearer_token=bearer_token)
        self.require_bearer_token(self.http_client.default_auth.merged_with(auth))
        params = self._build_list_params(limit=limit, cursor=cursor)
        data = await self.http_client.request(
            "GET",
            "/v1/tenants",
            params=params,
            auth=auth,
        )
        return TenantList.from_dict(dict(data))

    async def iter_all(
        self,
        *,
        bearer_token: str | None = None,
        page_size: int = 100,
    ) -> AsyncIterator[Tenant]:
        cursor: str | None = None
        while True:
            page = await self.list(
                bearer_token=bearer_token,
                limit=page_size,
                cursor=cursor,
            )
            for item in page.items:
                yield item
            if not page.has_more or page.next_cursor is None:
                return
            cursor = page.next_cursor

    async def create(
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

    @staticmethod
    def _build_list_params(
        *,
        limit: int | None,
        cursor: str | None,
    ) -> dict[str, str] | None:
        params: dict[str, str] = {}
        if limit is not None:
            if limit < 1 or limit > 100:
                raise ValidationError("limit must be between 1 and 100.")
            params["limit"] = str(limit)
        if cursor is not None:
            if not cursor.strip():
                raise ValidationError("cursor must not be empty.")
            params["cursor"] = cursor
        return params or None
