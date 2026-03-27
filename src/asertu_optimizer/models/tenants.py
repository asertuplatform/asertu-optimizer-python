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

    @classmethod
    def from_dict(cls, data: JsonDict) -> Tenant:
        return cls(
            tenant_id=data.get("tenant_id"),
            name=data.get("name"),
            role=data.get("role"),
            plan=data.get("plan"),
            is_default=data.get("is_default"),
        )


@dataclass(frozen=True, slots=True)
class TenantList:
    items: list[Tenant] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> TenantList:
        return cls(items=[Tenant.from_dict(item) for item in data.get("items", [])])


@dataclass(frozen=True, slots=True)
class TenantCreateRequest:
    name: str
    plan: str
    external_id: str | None = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TenantCreateResult:
    tenant: Tenant | None = None
    admin_api_key: str | None = None
    ingestion_api_key: str | None = None
