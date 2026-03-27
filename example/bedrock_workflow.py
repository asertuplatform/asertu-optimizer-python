from asertu_optimizer import AsertuOptimizerClient


def main() -> None:
    client = AsertuOptimizerClient.from_env()
    bedrock_response = {
        "modelId": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "usage": {
            "inputTokens": 150,
            "outputTokens": 60,
            "totalTokens": 210,
        },
    }
    result = client.events.track_bedrock_response(
        feature="classification",
        status="success",
        response=bedrock_response,
        metadata={"provider_sdk": "bedrock"},
    )
    print(result)


if __name__ == "__main__":
    main()
