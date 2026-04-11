"""Track an AI usage event with asertu Optimizer.

This is the most common SDK operation: recording an LLM call so that
Optimizer can aggregate cost, token usage, and performance metrics.

Prerequisites:
    pip install asertu-optimizer
    export ASERTU_TENANT_API_KEY=your-tenant-api-key

Usage:
    python track_event.py
"""

from __future__ import annotations

from asertu_optimizer import AsertuOptimizerClient


def main() -> None:
    # Build a client from environment variables.
    # The SDK reads ASERTU_TENANT_API_KEY (or OPTIMIZER_API_KEY) automatically.
    client = AsertuOptimizerClient.from_env()

    # --- Option A: track a generic LLM call ---
    result = client.events.track_llm_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="support_chat",
        input_tokens=1200,
        output_tokens=800,
        status="success",
        metadata={"source": "quickstart"},
    )
    print("Tracked generic LLM call:", result)

    # --- Option B: track from a real OpenAI response dict ---
    openai_response = {
        "model": "gpt-4.1-mini",
        "usage": {
            "prompt_tokens": 500,
            "completion_tokens": 150,
            "total_tokens": 650,
        },
    }
    result = client.events.track_openai_response(
        feature="support_chat",
        status="success",
        response=openai_response,
    )
    print("Tracked OpenAI response:", result)


if __name__ == "__main__":
    main()
