"""Read tenant-scoped analytics from asertu Optimizer.

This script demonstrates authenticated reads: listing tenants, querying
the analytics dashboard, and fetching cost history.

Prerequisites:
    pip install asertu-optimizer
    export ASERTU_BEARER_TOKEN=your-jwt-token
    export ASERTU_TENANT_ID=your-tenant-id

Usage:
    python read_analytics.py
"""

from __future__ import annotations

from pprint import pprint

from asertu_optimizer import AsertuOptimizerClient


def main() -> None:
    # For tenant-scoped reads the SDK needs a JWT bearer token and tenant ID.
    client = AsertuOptimizerClient.from_env()

    # List tenants available to the authenticated user.
    tenants = client.tenants.list(limit=5)
    print("Tenants (first page):")
    pprint(tenants)
    print()

    # Dashboard summary for today.
    summary = client.analytics.dashboard_summary(preset="today")
    print("Analytics summary (today):")
    pprint(summary)
    print()

    # Cost history for the last 7 days.
    history = client.history.daily_cost(preset="last_7_days")
    print("Daily cost (last 7 days):")
    pprint(history)


if __name__ == "__main__":
    main()
