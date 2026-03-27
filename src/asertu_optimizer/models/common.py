from __future__ import annotations

from dataclasses import dataclass
from datetime import date

DateLike = date | str


@dataclass(frozen=True, slots=True)
class DateRange:
    from_date: DateLike | None = None
    to_date: DateLike | None = None
    preset: str | None = None

    def to_query_params(self) -> dict[str, str]:
        params: dict[str, str] = {}
        if self.from_date is not None:
            params["from"] = (
                self.from_date.isoformat()
                if isinstance(self.from_date, date)
                else self.from_date
            )
        if self.to_date is not None:
            params["to"] = (
                self.to_date.isoformat() if isinstance(self.to_date, date) else self.to_date
            )
        if self.preset is not None:
            params["preset"] = self.preset
        return params
