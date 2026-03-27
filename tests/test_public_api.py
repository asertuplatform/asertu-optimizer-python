from __future__ import annotations

from pathlib import Path

import asertu_optimizer
from asertu_optimizer import AsertuOptimizerClient, AsyncAsertuOptimizerClient


def test_version_is_stable_release() -> None:
    assert asertu_optimizer.__version__ == "2.0.0"


def test_top_level_exports_exist() -> None:
    expected_exports = {
        "AsertuOptimizerClient",
        "AsyncAsertuOptimizerClient",
        "AsertuOptimizerError",
        "ApiError",
        "AuthenticationError",
        "BadRequestError",
        "ContractUnavailableError",
        "MissingCredentialsError",
        "PermissionDeniedError",
        "TransportError",
        "ValidationError",
        "InMemoryTelemetryCollector",
        "SdkTelemetryEvent",
        "__version__",
    }
    assert set(asertu_optimizer.__all__) == expected_exports
    for name in expected_exports:
        assert hasattr(asertu_optimizer, name)


def test_clients_expose_stable_resources() -> None:
    sync_client = AsertuOptimizerClient()
    async_client = AsyncAsertuOptimizerClient()

    for client in (sync_client, async_client):
        assert hasattr(client, "events")
        assert hasattr(client, "tenants")
        assert hasattr(client, "pricing")
        assert hasattr(client, "analytics")
        assert hasattr(client, "history")
        assert hasattr(client, "billing")
        assert hasattr(client, "settings")


def test_package_is_typed() -> None:
    marker = Path(asertu_optimizer.__file__).with_name("py.typed")
    assert marker.exists()
