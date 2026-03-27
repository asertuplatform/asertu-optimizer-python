from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass(frozen=True, slots=True)
class TimeSeriesPoint:
    bucket: str | None = None
    value: float | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> TimeSeriesPoint:
        return cls(
            bucket=data.get("bucket"),
            value=data.get("value"),
        )


@dataclass(frozen=True, slots=True)
class TimeSeries:
    tenant_id: str | None = None
    granularity: str | None = None
    points: list[TimeSeriesPoint] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> TimeSeries:
        return cls(
            tenant_id=data.get("tenant_id"),
            granularity=data.get("granularity"),
            points=[TimeSeriesPoint.from_dict(item) for item in data.get("points", [])],
        )
