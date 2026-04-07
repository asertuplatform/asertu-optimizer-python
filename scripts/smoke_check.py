from __future__ import annotations

import os
import sys
from collections.abc import Sequence

from asertu_optimizer import AsertuOptimizerClient


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_env(*names: str, default: str | None = None) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def main() -> int:
    base_url = (
        get_env("ASERTU_BASE_URL", "OPTIMIZER_BASE_URL", default="https://api.optimizer.asertu.ai")
        or "https://api.optimizer.asertu.ai"
    )
    tenant_api_key = get_env("ASERTU_TENANT_API_KEY", "OPTIMIZER_API_KEY")
    bearer_token = get_env("ASERTU_BEARER_TOKEN", "OPTIMIZER_BEARER_TOKEN")
    tenant_id = get_env("ASERTU_TENANT_ID", "OPTIMIZER_TENANT_ID")

    if not tenant_api_key and not bearer_token:
        raise RuntimeError(
            "Missing credentials. Set ASERTU_TENANT_API_KEY/OPTIMIZER_API_KEY "
            "for ingestion, or ASERTU_BEARER_TOKEN/OPTIMIZER_BEARER_TOKEN for JWT flows."
        )

    client = AsertuOptimizerClient(
        base_url=base_url,
        bearer_token=bearer_token,
        tenant_id=tenant_id,
        tenant_api_key=tenant_api_key,
    )

    if client.auth.tenant_api_key:
        events: Sequence[tuple[str, int, int]] = (
            ("prod_smoke_overview", 120, 80),
            ("prod_smoke_usage", 240, 120),
            ("prod_smoke_history", 180, 90),
        )
        for feature, input_tokens, output_tokens in events:
            response = client.events.track_openai_call(
                model="gpt-4.1-mini",
                feature=feature,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                status="success",
                metadata={
                    "source": "scripts.smoke_check",
                    "environment": "prod",
                },
            )
            print(
                "event accepted",
                f"feature={feature}",
                f"tenant_id={response.tenant_id}",
                f"s3_key={response.s3_key}",
            )

    if client.auth.bearer_token:
        tenants = client.tenants.list()
        print(f"tenants={len(tenants.items)}")

    if client.auth.tenant_id and client.auth.bearer_token:
        summary = client.analytics.dashboard_summary(preset="today")
        print(f"summary_total_requests={summary.total_requests}")

        catalog = client.billing.catalog()
        print(f"billing_plans={len(catalog.plans)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"smoke check failed: {exc}", file=sys.stderr)
        raise
