from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class ProviderUsage:
    provider: str
    model: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None


def _read_value(source: Any, *path: str) -> Any:
    current = source
    for key in path:
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(key)
            continue
        current = getattr(current, key, None)
    return current


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValidationError("Boolean values are not valid token counts.")
    return int(value)


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValidationError("Boolean values are not valid costs.")
    return float(value)


def extract_openai_usage(response: Any, *, model: str | None = None) -> ProviderUsage:
    resolved_model = model or _read_value(response, "model")
    input_tokens = _coerce_int(
        _read_value(response, "usage", "prompt_tokens")
        or _read_value(response, "usage", "input_tokens")
    )
    output_tokens = _coerce_int(
        _read_value(response, "usage", "completion_tokens")
        or _read_value(response, "usage", "output_tokens")
    )
    total_tokens = _coerce_int(_read_value(response, "usage", "total_tokens"))
    return ProviderUsage(
        provider="openai",
        model=resolved_model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


def extract_anthropic_usage(response: Any, *, model: str | None = None) -> ProviderUsage:
    resolved_model = model or _read_value(response, "model")
    input_tokens = _coerce_int(_read_value(response, "usage", "input_tokens"))
    output_tokens = _coerce_int(_read_value(response, "usage", "output_tokens"))
    total_tokens = (
        _coerce_int(_read_value(response, "usage", "total_tokens"))
        or (
            (input_tokens or 0) + (output_tokens or 0)
            if input_tokens is not None or output_tokens is not None
            else None
        )
    )
    return ProviderUsage(
        provider="anthropic",
        model=resolved_model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


def extract_bedrock_usage(response: Any, *, model: str | None = None) -> ProviderUsage:
    resolved_model = (
        model
        or _read_value(response, "modelId")
        or _read_value(response, "model_id")
        or _read_value(response, "model")
    )
    input_tokens = _coerce_int(
        _read_value(response, "usage", "inputTokens")
        or _read_value(response, "usage", "input_tokens")
    )
    output_tokens = _coerce_int(
        _read_value(response, "usage", "outputTokens")
        or _read_value(response, "usage", "output_tokens")
    )
    total_tokens = _coerce_int(
        _read_value(response, "usage", "totalTokens")
        or _read_value(response, "usage", "total_tokens")
    )
    return ProviderUsage(
        provider="bedrock",
        model=resolved_model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


def extract_provider_usage(
    provider: str,
    response: Any,
    *,
    model: str | None = None,
) -> ProviderUsage:
    normalized_provider = provider.strip().lower()
    if normalized_provider == "openai":
        return extract_openai_usage(response, model=model)
    if normalized_provider == "anthropic":
        return extract_anthropic_usage(response, model=model)
    if normalized_provider == "bedrock":
        return extract_bedrock_usage(response, model=model)
    raise ValidationError(f"Unsupported provider '{provider}' for instrumentation helpers.")
