from __future__ import annotations

from collections.abc import Iterator

from ..exceptions import ValidationError
from ..models.tenants import Tenant, TenantList
from .base import BaseResource


class TenantsResource(BaseResource):
    def list(
        self,
        *,
        bearer_token: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> TenantList:
        auth = self.build_auth(bearer_token=bearer_token)
        self.require_bearer_token(self.http_client.default_auth.merged_with(auth))
        params = self._build_list_params(limit=limit, cursor=cursor)
        data = self.http_client.request(
            "GET",
            "/v1/tenants",
            params=params,
            auth=auth,
        )
        return TenantList.from_dict(dict(data))

    def iter_all(
        self,
        *,
        bearer_token: str | None = None,
        page_size: int = 100,
    ) -> Iterator[Tenant]:
        cursor: str | None = None
        while True:
            page = self.list(
                bearer_token=bearer_token,
                limit=page_size,
                cursor=cursor,
            )
            yield from page.items
            if not page.has_more or page.next_cursor is None:
                return
            cursor = page.next_cursor

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
