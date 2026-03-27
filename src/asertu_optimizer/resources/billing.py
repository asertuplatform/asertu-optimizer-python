from __future__ import annotations

from ..models.billing import BillingCatalog, BillingCheckoutRequest, BillingCheckoutResult
from .base import BaseResource


class BillingResource(BaseResource):
    def catalog(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> BillingCatalog:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = self.http_client.request("GET", "/v1/billing/catalog", auth=auth)
        return BillingCatalog.from_dict(dict(data))

    def start_checkout(
        self,
        *,
        plan_id: str,
        provider: str,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> BillingCheckoutResult:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        payload = BillingCheckoutRequest(plan_id=plan_id, provider=provider).to_payload()
        data = self.http_client.request(
            "POST",
            "/v1/billing/checkout",
            json_body=payload,
            auth=auth,
        )
        return BillingCheckoutResult.from_dict(dict(data))
