from __future__ import annotations

import argparse
import asyncio
from pprint import pprint

from asertu_optimizer import AsyncAsertuOptimizerClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="asertu Optimizer async playground")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary_parser = subparsers.add_parser("analytics-summary")
    summary_parser.add_argument("--preset", default="today")
    summary_parser.add_argument("--from-date")
    summary_parser.add_argument("--to-date")

    event_parser = subparsers.add_parser("track-openai-event")
    event_parser.add_argument("--model", default="gpt-4.1-mini")
    event_parser.add_argument("--feature", default="support_chat")

    return parser


async def main() -> None:
    args = build_parser().parse_args()
    client = AsyncAsertuOptimizerClient.from_env()

    try:
        if args.command == "analytics-summary":
            summary = await client.analytics.dashboard_summary(
                preset=args.preset,
                from_date=args.from_date,
                to_date=args.to_date,
            )
            pprint(summary)
            return

        if args.command == "track-openai-event":
            event_result = await client.events.track_openai_call(
                model=args.model,
                feature=args.feature,
                input_tokens=100,
                output_tokens=50,
                status="success",
                metadata={"source": "example.async_playground"},
            )
            pprint(event_result)
            return
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
