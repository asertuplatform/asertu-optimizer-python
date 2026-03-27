# Referencia de API

## Cliente

- `AsertuOptimizerClient.events`
- `AsertuOptimizerClient.tenants`
- `AsertuOptimizerClient.pricing`
- `AsertuOptimizerClient.analytics`
- `AsertuOptimizerClient.history`
- `AsertuOptimizerClient.billing`
- `AsertuOptimizerClient.settings`
- `AsertuOptimizerClient.from_env()`
- `AsyncAsertuOptimizerClient.*`

## Events

- `ingest(event, tenant_api_key=None)`
- `track_llm_call(provider, model, feature, status, ...)`
- `track_openai_call(...)`
- `track_anthropic_call(...)`
- `track_bedrock_call(...)`
- `track_openai_response(...)`
- `track_anthropic_response(...)`
- `track_bedrock_response(...)`

## Tenants

- `list(bearer_token=None)`
- `create(...)`
  Actualmente devuelve `ContractUnavailableError` hasta que exista contrato oficial.

## Pricing

- `upsert(rule, admin_api_key=None)`
  Actualmente devuelve `ContractUnavailableError` hasta que exista contrato oficial.

## Analytics

- `dashboard_summary(...)`
- `usage_by_feature(...)`
- `usage_by_model(...)`
- `insights_basic(...)`
- `insights_advanced(...)`
- `recommendations(...)`

## History

- `daily_cost(...)`
- `daily_tokens(...)`
- `cost_by_feature(...)`
- `cost_by_model(...)`

## Billing

- `catalog(...)`
- `start_checkout(...)`

## Settings

- `workspace(...)`
- `create_access_request(...)`
- `invitations(...)`
- `invite_member(...)`
- `manage_invitation(...)`
- `decide_access_request(...)`
- `manage_membership(...)`
