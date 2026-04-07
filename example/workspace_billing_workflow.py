from __future__ import annotations

from pprint import pprint

from asertu_optimizer import AsertuOptimizerClient, InMemoryTelemetryCollector


def main() -> None:
    telemetry = InMemoryTelemetryCollector()
    client = AsertuOptimizerClient(
        base_url="https://api.optimizer.asertu.ai",
        bearer_token="jwt-token",
        tenant_id="tenant-123",
        telemetry_handler=telemetry,
    )

    workspace = client.settings.workspace()
    invitations = client.settings.invitations()
    catalog = client.billing.catalog()

    pprint(workspace)
    pprint(invitations)
    pprint(catalog)
    pprint(telemetry.events)


if __name__ == "__main__":
    main()
