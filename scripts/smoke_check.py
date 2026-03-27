from __future__ import annotations

import os
import sys

from asertu_optimizer import AsertuOptimizerClient


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    base_url = os.getenv("ASERTU_BASE_URL", "https://api.dev.asertu.ai")
    bearer_token = require_env("ASERTU_BEARER_TOKEN")

    client = AsertuOptimizerClient(
        base_url=base_url,
        bearer_token=bearer_token,
        tenant_id=os.getenv("ASERTU_TENANT_ID"),
        tenant_api_key=os.getenv("ASERTU_TENANT_API_KEY"),
    )

    tenants = client.tenants.list()
    print(f"tenants={len(tenants.items)}")

    if client.auth.tenant_id:
        summary = client.analytics.dashboard_summary(preset="today")
        print(f"summary_total_requests={summary.total_requests}")

        catalog = client.billing.catalog()
        print(f"billing_plans={len(catalog.plans)}")

    if client.auth.tenant_api_key:
        response = client.events.track_openai_call(
            model="gpt-4.1-mini",
            feature="smoke_test",
            input_tokens=10,
            output_tokens=5,
            status="success",
            metadata={"source": "github_actions_smoke"},
        )
        print(f"event_tenant_id={response.tenant_id}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"smoke check failed: {exc}", file=sys.stderr)
        raise
