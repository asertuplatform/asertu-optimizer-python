from __future__ import annotations

from ..models.analytics import UsageBreakdown
from ..models.common import DateRange, TimeSeriesQuery
from ..models.history import TimeSeries
from .base import AsyncBaseResource


class AsyncHistoryResource(AsyncBaseResource):
    async def daily_cost(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
        granularity: str | None = None,
    ) -> TimeSeries:
        data = await self._time_series(
            "/v1/history/daily-cost",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=TimeSeriesQuery(
                from_date=from_date,
                to_date=to_date,
                preset=preset,
                granularity=granularity,
            ),
        )
        return TimeSeries.from_dict(data)

    async def daily_tokens(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
        granularity: str | None = None,
    ) -> TimeSeries:
        data = await self._time_series(
            "/v1/history/daily-tokens",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=TimeSeriesQuery(
                from_date=from_date,
                to_date=to_date,
                preset=preset,
                granularity=granularity,
            ),
        )
        return TimeSeries.from_dict(data)

    async def cost_by_feature(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> UsageBreakdown:
        data = await self._breakdown(
            "/v1/history/cost-by-feature",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return UsageBreakdown.from_dict(data)

    async def cost_by_model(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        preset: str | None = None,
    ) -> UsageBreakdown:
        data = await self._breakdown(
            "/v1/history/cost-by-model",
            tenant_id=tenant_id,
            bearer_token=bearer_token,
            query=DateRange(from_date=from_date, to_date=to_date, preset=preset),
        )
        return UsageBreakdown.from_dict(data)

    async def _time_series(
        self,
        path: str,
        *,
        tenant_id: str | None,
        bearer_token: str | None,
        query: TimeSeriesQuery,
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

    async def _breakdown(
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
