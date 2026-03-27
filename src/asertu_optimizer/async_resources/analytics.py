from __future__ import annotations

from ..models.analytics import Insights, Recommendations, Summary, UsageBreakdown
from ..models.common import DateRange
from .base import AsyncBaseResource


class AsyncAnalyticsResource(AsyncBaseResource):
    async def dashboard_summary(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> Summary:
        data = await self._tenant_read(
            "/v1/dashboard/summary",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return Summary.from_dict(data)

    async def usage_by_feature(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> UsageBreakdown:
        data = await self._tenant_read(
            "/v1/usage/by-feature",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return UsageBreakdown.from_dict(data)

    async def usage_by_model(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> UsageBreakdown:
        data = await self._tenant_read(
            "/v1/usage/by-model",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return UsageBreakdown.from_dict(data)

    async def insights_basic(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> Insights:
        data = await self._tenant_read(
            "/v1/insights/basic",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return Insights.from_dict(data)

    async def insights_advanced(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> Insights:
        data = await self._tenant_read(
            "/v1/insights/advanced",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return Insights.from_dict(data)

    async def recommendations(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> Recommendations:
        data = await self._tenant_read(
            "/v1/recommendations",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return Recommendations.from_dict(data)

    async def _tenant_read(
        self,
        path: str,
        *,
        tenant_id: str | None,
        bearer_token: str | None,
        query: DateRange,
    ) -> dict[str, object]:
        auth = self.build_auth(
            bearer_token=bearer_token,
            tenant_id=tenant_id,
        )
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = await self.http_client.request(
            "GET",
            path,
            params=query.to_query_params(),
            auth=auth,
        )
        return dict(data)
