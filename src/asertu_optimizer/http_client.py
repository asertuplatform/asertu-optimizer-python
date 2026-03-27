from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from .auth import RequestAuth
from .config import ClientConfig
from .exceptions import (
    ApiError,
    AuthenticationError,
    BadRequestError,
    PermissionDeniedError,
    TransportError,
)

JsonMapping = Mapping[str, Any]


class AsertuHttpClient:
    def __init__(
        self,
        *,
        config: ClientConfig,
        auth: RequestAuth,
        client: httpx.Client | None = None,
    ) -> None:
        self._config = config
        self._auth = auth
        self._client = client or httpx.Client(
            base_url=config.base_url.rstrip("/"),
            timeout=config.timeout,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": config.user_agent,
            },
        )
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, str] | None = None,
        json_body: JsonMapping | None = None,
        auth: RequestAuth | None = None,
    ) -> JsonMapping:
        merged_auth = self._auth.merged_with(auth)
        headers = merged_auth.headers()
        retries_remaining = self._config.max_retries if method.upper() == "GET" else 0

        while True:
            try:
                response = self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_body,
                    headers=headers,
                )
            except httpx.HTTPError as exc:
                if retries_remaining > 0:
                    retries_remaining -= 1
                    continue
                raise TransportError(f"Request to {path} failed: {exc}") from exc

            if response.status_code >= 500 and retries_remaining > 0:
                retries_remaining -= 1
                continue

            return self._handle_response(response)

    @staticmethod
    def _handle_response(response: httpx.Response) -> JsonMapping:
        try:
            data = response.json() if response.content else {}
        except ValueError:
            data = {"message": response.text}

        if 200 <= response.status_code < 300:
            return data

        message = data.get("message", "Asertu Optimizer API request failed")
        if response.status_code == 400:
            raise BadRequestError(message, status_code=response.status_code, response_body=data)
        if response.status_code == 401:
            raise AuthenticationError(message, status_code=response.status_code, response_body=data)
        if response.status_code == 403:
            raise PermissionDeniedError(
                message,
                status_code=response.status_code,
                response_body=data,
            )
        raise ApiError(message, status_code=response.status_code, response_body=data)
