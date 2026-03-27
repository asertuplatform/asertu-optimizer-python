from __future__ import annotations

import argparse
from pprint import pprint

from asertu_optimizer import AsertuOptimizerClient


def build_client() -> AsertuOptimizerClient:
    return AsertuOptimizerClient.from_env()


def track_event(client: AsertuOptimizerClient, _: argparse.Namespace) -> None:
    result = client.events.track_llm_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="support_chat",
        input_tokens=1200,
        output_tokens=800,
        status="success",
        metadata={"source": "example.playground"},
    )
    pprint(result)


def track_openai_event(client: AsertuOptimizerClient, _: argparse.Namespace) -> None:
    result = client.events.track_openai_call(
        model="gpt-4.1-mini",
        feature="support_chat",
        input_tokens=1200,
        output_tokens=800,
        status="success",
        metadata={"source": "example.playground", "helper": "track_openai_call"},
    )
    pprint(result)


def track_openai_response(client: AsertuOptimizerClient, _: argparse.Namespace) -> None:
    result = client.events.track_openai_response(
        feature="support_chat",
        status="success",
        response={
            "model": "gpt-4.1-mini",
            "usage": {
                "prompt_tokens": 1200,
                "completion_tokens": 800,
                "total_tokens": 2000,
            },
        },
        metadata={"source": "example.playground", "helper": "track_openai_response"},
    )
    pprint(result)


def list_tenants_page(client: AsertuOptimizerClient, args: argparse.Namespace) -> None:
    pprint(client.tenants.list(limit=args.limit, cursor=args.cursor))


def list_all_tenants(client: AsertuOptimizerClient, args: argparse.Namespace) -> None:
    pprint(list(client.tenants.iter_all(page_size=args.page_size)))


def analytics_summary(client: AsertuOptimizerClient, args: argparse.Namespace) -> None:
    pprint(
        client.analytics.dashboard_summary(
            preset=args.preset,
            from_date=args.from_date,
            to_date=args.to_date,
        )
    )


def history_daily_cost(client: AsertuOptimizerClient, args: argparse.Namespace) -> None:
    pprint(
        client.history.daily_cost(
            preset=args.preset,
            from_date=args.from_date,
            to_date=args.to_date,
            granularity=args.granularity,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Asertu Optimizer SDK playground")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("track-event")
    subparsers.add_parser("track-openai-event")
    subparsers.add_parser("track-openai-response")
    list_tenants_parser = subparsers.add_parser("list-tenants")
    list_tenants_parser.add_argument("--limit", type=int)
    list_tenants_parser.add_argument("--cursor")

    list_all_tenants_parser = subparsers.add_parser("list-all-tenants")
    list_all_tenants_parser.add_argument("--page-size", type=int, default=100)

    analytics_parser = subparsers.add_parser("analytics-summary")
    analytics_parser.add_argument("--preset", default="today")
    analytics_parser.add_argument("--from-date")
    analytics_parser.add_argument("--to-date")

    history_parser = subparsers.add_parser("history-daily-cost")
    history_parser.add_argument("--preset", default="last_7_days")
    history_parser.add_argument("--from-date")
    history_parser.add_argument("--to-date")
    history_parser.add_argument("--granularity", default="daily")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    client = build_client()

    handlers = {
        "track-event": track_event,
        "track-openai-event": track_openai_event,
        "track-openai-response": track_openai_response,
        "list-tenants": list_tenants_page,
        "list-all-tenants": list_all_tenants,
        "analytics-summary": analytics_summary,
        "history-daily-cost": history_daily_cost,
    }
    handlers[args.command](client, args)


if __name__ == "__main__":
    main()
