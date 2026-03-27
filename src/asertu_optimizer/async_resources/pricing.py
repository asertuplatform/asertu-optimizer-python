from __future__ import annotations

from ..exceptions import ContractUnavailableError
from ..models.pricing import PricingRule
from .base import AsyncBaseResource


class AsyncPricingResource(AsyncBaseResource):
    async def upsert(
        self,
        rule: PricingRule,
        *,
        admin_api_key: str | None = None,
    ) -> None:
        _ = rule
        _ = admin_api_key
        raise ContractUnavailableError(
            "Pricing upsert is not implemented because the admin pricing endpoint "
            "is not published in the current OpenAPI contract yet."
        )
