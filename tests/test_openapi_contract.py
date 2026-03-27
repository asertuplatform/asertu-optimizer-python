from __future__ import annotations

import os
import subprocess
from typing import Any, cast
from urllib.request import urlopen

import pytest
import yaml

CONTRACT_URL = os.getenv(
    "ASERTU_CONTRACT_URL",
    "https://optimizer.dev.asertu.ai/openapi/optimizer-openapi.yaml",
)
RUN_LIVE_CONTRACT_TEST = os.getenv("ASERTU_RUN_LIVE_CONTRACT_TEST") == "1"


def fetch_contract() -> dict[str, object]:
    try:
        completed = subprocess.run(
            ["curl", "-fsSL", CONTRACT_URL],
            capture_output=True,
            check=True,
            text=True,
        )
        data = yaml.safe_load(completed.stdout)
    except Exception:
        with urlopen(CONTRACT_URL, timeout=20) as response:
            data = yaml.safe_load(response.read().decode())
    return cast(dict[str, object], data)


def test_openapi_contract_version_and_paths() -> None:
    if not RUN_LIVE_CONTRACT_TEST:
        pytest.skip("Set ASERTU_RUN_LIVE_CONTRACT_TEST=1 to run live contract checks.")
    contract = fetch_contract()
    info = cast(dict[str, Any], contract["info"])
    paths = cast(dict[str, Any], contract["paths"])

    assert contract["openapi"] == "3.0.3"
    assert info["version"] == "1.23.23"
    assert "/v1/events" in paths
    assert "/v1/tenants" in paths
    assert "/v1/settings/workspace" in paths
    assert "/v1/billing/catalog" in paths
    tenant_parameters = cast(list[dict[str, Any]], paths["/v1/tenants"]["get"]["parameters"])
    components = cast(dict[str, Any], contract["components"])
    component_parameters = cast(dict[str, Any], components["parameters"])
    parameter_names = [
        cast(dict[str, Any], component_parameters[item["$ref"].split("/")[-1]])["name"]
        for item in tenant_parameters
    ]
    assert parameter_names == ["limit", "cursor"]


def test_openapi_contract_exposes_expected_schemas() -> None:
    if not RUN_LIVE_CONTRACT_TEST:
        pytest.skip("Set ASERTU_RUN_LIVE_CONTRACT_TEST=1 to run live contract checks.")
    contract = fetch_contract()
    components = cast(dict[str, Any], contract["components"])
    schemas = cast(dict[str, Any], components["schemas"])
    tenant_schema = cast(dict[str, Any], schemas["Tenant"])
    tenant_properties = cast(dict[str, Any], tenant_schema["properties"])

    assert "TenantsResponse" in schemas
    assert "Pagination" in schemas
    assert "WorkspaceSettingsResponse" in schemas
    assert "BillingCatalogResponse" in schemas

    assert "plan_id" in tenant_properties
    assert "subscription_status" in tenant_properties
    response_properties = cast(dict[str, Any], schemas["TenantsResponse"]["properties"])
    assert "pagination" in response_properties
