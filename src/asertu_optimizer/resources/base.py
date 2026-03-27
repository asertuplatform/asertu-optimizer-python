from __future__ import annotations

from dataclasses import dataclass

from ..auth import RequestAuth
from ..exceptions import MissingCredentialsError
from ..http_client import AsertuHttpClient


@dataclass(slots=True)
class BaseResource:
    http_client: AsertuHttpClient

    @staticmethod
    def build_auth(
        *,
        tenant_api_key: str | None = None,
        bearer_token: str | None = None,
        tenant_id: str | None = None,
    ) -> RequestAuth | None:
        if not any((tenant_api_key, bearer_token, tenant_id)):
            return None
        return RequestAuth(
            tenant_api_key=tenant_api_key,
            bearer_token=bearer_token,
            tenant_id=tenant_id,
        )

    def require_tenant_api_key(self, auth: RequestAuth | None) -> None:
        if auth is None or not auth.has_api_key:
            raise MissingCredentialsError("This operation requires a tenant_api_key.")

    def require_bearer_token(self, auth: RequestAuth | None) -> None:
        if auth is None or not auth.has_bearer_token:
            raise MissingCredentialsError("This operation requires a bearer_token.")

    def require_tenant_scope(self, auth: RequestAuth | None) -> None:
        self.require_bearer_token(auth)
        if auth is None or not auth.tenant_id:
            raise MissingCredentialsError(
                "This operation requires tenant_id together with bearer_token."
            )
