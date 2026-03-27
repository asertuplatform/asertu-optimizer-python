from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass(frozen=True, slots=True)
class Summary:
    tenant_id: str | None = None
    from_date: str | None = None
    to_date: str | None = None
    total_requests: int | None = None
    total_tokens: int | None = None
    total_cost: float | None = None
    total_errors: int | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> Summary:
        return cls(
            tenant_id=data.get("tenant_id"),
            from_date=data.get("from"),
            to_date=data.get("to"),
            total_requests=data.get("total_requests"),
            total_tokens=data.get("total_tokens"),
            total_cost=data.get("total_cost"),
            total_errors=data.get("total_errors"),
        )


@dataclass(frozen=True, slots=True)
class UsageBreakdownItem:
    key: str | None = None
    label: str | None = None
    requests: int | None = None
    tokens: int | None = None
    cost: float | None = None
    errors: int | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> UsageBreakdownItem:
        return cls(
            key=data.get("key"),
            label=data.get("label"),
            requests=data.get("requests"),
            tokens=data.get("tokens"),
            cost=data.get("cost"),
            errors=data.get("errors"),
        )


@dataclass(frozen=True, slots=True)
class UsageBreakdown:
    tenant_id: str | None = None
    from_date: str | None = None
    to_date: str | None = None
    items: list[UsageBreakdownItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> UsageBreakdown:
        return cls(
            tenant_id=data.get("tenant_id"),
            from_date=data.get("from"),
            to_date=data.get("to"),
            items=[UsageBreakdownItem.from_dict(item) for item in data.get("items", [])],
        )


@dataclass(frozen=True, slots=True)
class InsightItem:
    title: str | None = None
    level: str | None = None
    summary: str | None = None
    details: JsonDict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: JsonDict) -> InsightItem:
        return cls(
            title=data.get("title"),
            level=data.get("level"),
            summary=data.get("summary"),
            details=data.get("details") or {},
        )


@dataclass(frozen=True, slots=True)
class Insights:
    tenant_id: str | None = None
    items: list[InsightItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> Insights:
        return cls(
            tenant_id=data.get("tenant_id"),
            items=[InsightItem.from_dict(item) for item in data.get("items", [])],
        )


@dataclass(frozen=True, slots=True)
class RecommendationItem:
    title: str | None = None
    summary: str | None = None
    impact: str | None = None
    priority: str | None = None
    metadata: JsonDict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: JsonDict) -> RecommendationItem:
        return cls(
            title=data.get("title"),
            summary=data.get("summary"),
            impact=data.get("impact"),
            priority=data.get("priority"),
            metadata=data.get("metadata") or {},
        )


@dataclass(frozen=True, slots=True)
class Recommendations:
    tenant_id: str | None = None
    items: list[RecommendationItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> Recommendations:
        return cls(
            tenant_id=data.get("tenant_id"),
            items=[RecommendationItem.from_dict(item) for item in data.get("items", [])],
        )
