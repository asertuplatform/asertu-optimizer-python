from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass(frozen=True, slots=True)
class Tenant:
    tenant_id: str | None = None
    name: str | None = None
    role: str | None = None
    plan: str | None = None
    is_default: bool | None = None
    plan_id: str | None = None
    plan_name: str | None = None
    subscription_status: str | None = None
    renewal_date: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> Tenant:
        return cls(
            tenant_id=data.get("tenant_id"),
            name=data.get("name"),
            role=data.get("role"),
            plan=data.get("plan"),
            is_default=data.get("is_default"),
            plan_id=data.get("plan_id"),
            plan_name=data.get("plan_name"),
            subscription_status=data.get("subscription_status"),
            renewal_date=data.get("renewal_date"),
        )


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    sub: str | None = None
    email: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> AuthenticatedUser:
        return cls(
            sub=data.get("sub"),
            email=data.get("email"),
        )


@dataclass(frozen=True, slots=True)
class Pagination:
    limit: int | None = None
    next_cursor: str | None = None
    has_more: bool = False
    total_items: int | None = None
    missing_fields: list[str] = field(default_factory=list)
    required_information: list[str] = field(default_factory=list)
    error: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> Pagination:
        return cls(
            limit=data.get("limit"),
            next_cursor=data.get("next_cursor"),
            has_more=bool(data.get("has_more")),
            total_items=data.get("total_items"),
            missing_fields=list(data.get("missing_fields") or []),
            required_information=list(data.get("required_information") or []),
            error=data.get("error"),
        )


@dataclass(frozen=True, slots=True)
class TenantList:
    tenants: list[Tenant] = field(default_factory=list)
    user: AuthenticatedUser | None = None
    pagination: Pagination | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> TenantList:
        raw_items = data.get("tenants", data.get("items", [])) or []
        user = data.get("user")
        pagination = data.get("pagination")
        return cls(
            tenants=[Tenant.from_dict(item) for item in raw_items],
            user=AuthenticatedUser.from_dict(user) if isinstance(user, dict) else None,
            pagination=Pagination.from_dict(pagination) if isinstance(pagination, dict) else None,
        )

    @property
    def items(self) -> list[Tenant]:
        return self.tenants

    @property
    def next_cursor(self) -> str | None:
        return self.pagination.next_cursor if self.pagination is not None else None

    @property
    def has_more(self) -> bool:
        return self.pagination.has_more if self.pagination is not None else False
