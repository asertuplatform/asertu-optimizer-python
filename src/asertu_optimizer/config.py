from __future__ import annotations

from dataclasses import dataclass

DEFAULT_BASE_URL = "https://api.dev.asertu.ai"
DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_USER_AGENT = "asertu-optimizer-python/1.2.0"


@dataclass(frozen=True, slots=True)
class ClientConfig:
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT
    max_retries: int = DEFAULT_MAX_RETRIES
    user_agent: str = DEFAULT_USER_AGENT

    def __post_init__(self) -> None:
        if self.timeout <= 0:
            raise ValueError("timeout must be greater than 0")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
