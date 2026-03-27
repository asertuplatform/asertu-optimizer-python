from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass(frozen=True, slots=True)
class BillingProviderStatus:
    provider: str | None = None
    enabled: bool | None = None
    configured: bool | None = None
    missing_fields: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> BillingProviderStatus:
        return cls(
            provider=data.get("provider"),
            enabled=data.get("enabled"),
            configured=data.get("configured"),
            missing_fields=list(data.get("missing_fields", [])),
        )


@dataclass(frozen=True, slots=True)
class TenantSubscription:
    tenant_id: str | None = None
    plan_id: str | None = None
    plan_name: str | None = None
    monthly_price: float | None = None
    currency: str | None = None
    subscription_status: str | None = None
    billing_cycle: str | None = None
    payment_provider: str | None = None
    renewal_date: str | None = None
    cleanup_required: bool | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> TenantSubscription:
        return cls(
            tenant_id=data.get("tenant_id"),
            plan_id=data.get("plan_id"),
            plan_name=data.get("plan_name"),
            monthly_price=data.get("monthly_price"),
            currency=data.get("currency"),
            subscription_status=data.get("subscription_status"),
            billing_cycle=data.get("billing_cycle"),
            payment_provider=data.get("payment_provider"),
            renewal_date=data.get("renewal_date"),
            cleanup_required=data.get("cleanup_required"),
        )


@dataclass(frozen=True, slots=True)
class BillingHistoryEntry:
    history_id: str | None = None
    source: str | None = None
    summary: str | None = None
    status: str | None = None
    provider: str | None = None
    provider_reference: str | None = None
    plan_id: str | None = None
    plan_name: str | None = None
    monthly_price: float | None = None
    currency: str | None = None
    actor_email: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> BillingHistoryEntry:
        return cls(**{field: data.get(field) for field in cls.__dataclass_fields__})


@dataclass(frozen=True, slots=True)
class BillingPlan:
    plan_id: str | None = None
    name: str | None = None
    tier_order: int | None = None
    currency: str | None = None
    monthly_price: float | None = None
    summary: str | None = None
    inherits_from: str | None = None
    highlights: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    limits: JsonDict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: JsonDict) -> BillingPlan:
        return cls(
            plan_id=data.get("plan_id"),
            name=data.get("name"),
            tier_order=data.get("tier_order"),
            currency=data.get("currency"),
            monthly_price=data.get("monthly_price"),
            summary=data.get("summary"),
            inherits_from=data.get("inherits_from"),
            highlights=list(data.get("highlights", [])),
            features=list(data.get("features", [])),
            limits=data.get("limits") or {},
        )


@dataclass(frozen=True, slots=True)
class BillingCatalog:
    tenant: JsonDict | None = None
    current_subscription: TenantSubscription | None = None
    plans: list[BillingPlan] = field(default_factory=list)
    payment_configs: JsonDict = field(default_factory=dict)
    provider_options: dict[str, BillingProviderStatus] = field(default_factory=dict)
    billing_history: list[BillingHistoryEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> BillingCatalog:
        provider_options = {
            key: BillingProviderStatus.from_dict(value)
            for key, value in (data.get("provider_options") or {}).items()
        }
        current_subscription_data = data.get("current_subscription")
        return cls(
            tenant=data.get("tenant"),
            current_subscription=(
                TenantSubscription.from_dict(current_subscription_data)
                if isinstance(current_subscription_data, dict)
                else None
            ),
            plans=[BillingPlan.from_dict(item) for item in data.get("plans", [])],
            payment_configs=data.get("payment_configs") or {},
            provider_options=provider_options,
            billing_history=[
                BillingHistoryEntry.from_dict(item) for item in data.get("billing_history", [])
            ],
        )


@dataclass(frozen=True, slots=True)
class BillingCheckoutRequest:
    plan_id: str
    provider: str

    def to_payload(self) -> JsonDict:
        return {
            "plan_id": self.plan_id,
            "provider": self.provider,
        }


@dataclass(frozen=True, slots=True)
class BillingCheckoutResult:
    message: str | None = None
    provider: str | None = None
    mode: str | None = None
    checkout_url: str | None = None
    session_id: str | None = None
    attempt_id: str | None = None
    tenant_id: str | None = None
    plan_id: str | None = None
    missing_fields: list[str] = field(default_factory=list)
    required_information: list[str] = field(default_factory=list)
    error: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> BillingCheckoutResult:
        return cls(
            message=data.get("message"),
            provider=data.get("provider"),
            mode=data.get("mode"),
            checkout_url=data.get("checkout_url"),
            session_id=data.get("session_id"),
            attempt_id=data.get("attempt_id"),
            tenant_id=data.get("tenant_id"),
            plan_id=data.get("plan_id"),
            missing_fields=list(data.get("missing_fields", [])),
            required_information=list(data.get("required_information", [])),
            error=data.get("error"),
        )
