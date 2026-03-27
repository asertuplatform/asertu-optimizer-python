from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

from ..exceptions import ValidationError

DateLike = date | str
Preset = Literal[
    "today",
    "yesterday",
    "last_7_days",
    "last_30_days",
    "last_90_days",
    "month_to_date",
]
Granularity = Literal["hourly", "daily", "monthly", "total"]

VALID_PRESETS = {
    "today",
    "yesterday",
    "last_7_days",
    "last_30_days",
    "last_90_days",
    "month_to_date",
}
VALID_GRANULARITIES = {"hourly", "daily", "monthly", "total"}


def _normalize_date_like(value: DateLike) -> str:
    return value.isoformat() if isinstance(value, date) else value


def validate_date_range(
    *,
    from_date: DateLike | None,
    to_date: DateLike | None,
    preset: str | None,
) -> None:
    if preset and (from_date is not None or to_date is not None):
        raise ValidationError("Use either preset or explicit from/to dates, not both.")
    if (from_date is None) ^ (to_date is None):
        raise ValidationError("from_date and to_date must be provided together.")
    if preset is not None and preset not in VALID_PRESETS:
        raise ValidationError(
            f"Invalid preset '{preset}'. Expected one of: {', '.join(sorted(VALID_PRESETS))}."
        )


def validate_granularity(granularity: str | None) -> None:
    if granularity is not None and granularity not in VALID_GRANULARITIES:
        raise ValidationError(
            "Invalid granularity "
            f"'{granularity}'. Expected one of: {', '.join(sorted(VALID_GRANULARITIES))}."
        )


@dataclass(frozen=True, slots=True)
class DateRange:
    from_date: DateLike | None = None
    to_date: DateLike | None = None
    preset: str | None = None

    def to_query_params(self) -> dict[str, str]:
        validate_date_range(
            from_date=self.from_date,
            to_date=self.to_date,
            preset=self.preset,
        )
        params: dict[str, str] = {}
        if self.from_date is not None:
            params["from"] = _normalize_date_like(self.from_date)
        if self.to_date is not None:
            params["to"] = _normalize_date_like(self.to_date)
        if self.preset is not None:
            params["preset"] = self.preset
        return params


@dataclass(frozen=True, slots=True)
class TimeSeriesQuery(DateRange):
    granularity: str | None = None

    def to_query_params(self) -> dict[str, str]:
        params = DateRange.to_query_params(self)
        validate_granularity(self.granularity)
        if self.granularity is not None:
            params["granularity"] = self.granularity
        return params
