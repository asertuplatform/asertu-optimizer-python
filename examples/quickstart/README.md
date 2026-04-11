# Quickstart: asertu Optimizer Python SDK

A minimal, self-contained project that shows how to install and use the
[asertu-optimizer](https://pypi.org/project/asertu-optimizer/) Python SDK.

## Setup

```bash
# 1. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install the SDK
pip install -r requirements.txt
```

## Configuration

Copy the environment template and fill in your credentials:

```bash
cp .env.example .env
```

The SDK reads credentials from environment variables automatically when you
call `AsertuOptimizerClient.from_env()`.

| Variable | Purpose |
|---|---|
| `ASERTU_TENANT_API_KEY` | Tenant API key for event ingestion |
| `ASERTU_BEARER_TOKEN` | JWT token for tenant-scoped reads |
| `ASERTU_TENANT_ID` | Tenant ID for tenant-scoped reads |

Load them before running the examples:

```bash
export $(grep -v '^#' .env | xargs)
```

## Examples

### Track an AI event

The most common operation: record an LLM call so Optimizer can track cost
and usage.

```bash
python track_event.py
```

This script shows two approaches:
- `track_llm_call()` for generic provider/model/token tracking
- `track_openai_response()` for passing an OpenAI response dict directly

### Read analytics

Query tenants, dashboard summary, and cost history with an authenticated
client.

```bash
python read_analytics.py
```

Requires `ASERTU_BEARER_TOKEN` and `ASERTU_TENANT_ID`.

## What next

- Browse the full [SDK documentation](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/README.md)
- See the [example playground](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/example/README.md) for provider-specific workflows (Anthropic, Bedrock) and async usage
- Check the published [OpenAPI contract](https://optimizer.asertu.ai/swagger/index.html) for all available endpoints
