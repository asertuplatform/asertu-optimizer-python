from asertu_optimizer import AsertuOptimizerClient


def main() -> None:
    client = AsertuOptimizerClient.from_env()
    anthropic_response = {
        "model": "claude-sonnet-4-20250514",
        "usage": {
            "input_tokens": 90,
            "output_tokens": 45,
        },
    }
    result = client.events.track_anthropic_response(
        feature="draft_generation",
        status="success",
        response=anthropic_response,
        metadata={"provider_sdk": "anthropic"},
    )
    print(result)


if __name__ == "__main__":
    main()
