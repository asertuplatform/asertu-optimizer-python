from asertu_optimizer import AsertuOptimizerClient


def main() -> None:
    client = AsertuOptimizerClient.from_env()
    openai_response = {
        "model": "gpt-4.1-mini",
        "usage": {
            "prompt_tokens": 120,
            "completion_tokens": 80,
            "total_tokens": 200,
        },
    }
    result = client.events.track_openai_response(
        feature="support_chat",
        status="success",
        response=openai_response,
        metadata={"provider_sdk": "openai"},
    )
    print(result)


if __name__ == "__main__":
    main()
