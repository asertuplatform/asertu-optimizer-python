from asertu_optimizer import AsertuOptimizerClient


def main() -> None:
    client = AsertuOptimizerClient(
        base_url="https://api.dev.asertu.ai",
        tenant_api_key="tenant-key",
    )
    result = client.events.track_llm_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="support_chat",
        input_tokens=1200,
        output_tokens=800,
        status="success",
        metadata={"environment": "dev"},
    )
    print(result)


if __name__ == "__main__":
    main()
