from asertu_optimizer import AsertuOptimizerClient


def main() -> None:
    client = AsertuOptimizerClient(
        base_url="https://api.dev.asertu.ai",
        bearer_token="jwt-token",
    )
    tenants = client.tenants.list()
    for tenant in tenants.items:
        print(tenant)


if __name__ == "__main__":
    main()
