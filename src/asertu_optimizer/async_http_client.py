from __future__ import annotations

from collections.abc import Mapping
from time import perf_counter
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
from .telemetry import SdkTelemetryEvent

JsonMapping = Mapping[str, Any]


class AsyncAsertuHttpClient:
    def __init__(
        self,
        *,
        config: ClientConfig,
        auth: RequestAuth,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._config = config
        self._auth = auth
        self._client = client or httpx.AsyncClient(
            base_url=config.base_url.rstrip("/"),
            timeout=config.timeout,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": config.user_agent,
            },
        )
        self._owns_client = client is None

    @property
    def default_auth(self) -> RequestAuth:
        return self._auth

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def request(
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
            started_at = perf_counter()
            try:
                response = await self._client.request(
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
                self._emit_telemetry(
                    method=method,
                    path=path,
                    duration_ms=(perf_counter() - started_at) * 1000,
                    success=False,
                    status_code=None,
                    error_type=type(exc).__name__,
                )
                raise TransportError(f"Request to {path} failed: {exc}") from exc

            if response.status_code >= 500 and retries_remaining > 0:
                retries_remaining -= 1
                continue

            self._emit_telemetry(
                method=method,
                path=path,
                duration_ms=(perf_counter() - started_at) * 1000,
                success=200 <= response.status_code < 300,
                status_code=response.status_code,
                request_id=response.headers.get("x-request-id"),
            )

            return self._handle_response(response)

    def _emit_telemetry(
        self,
        *,
        method: str,
        path: str,
        duration_ms: float,
        success: bool,
        status_code: int | None,
        error_type: str | None = None,
        request_id: str | None = None,
    ) -> None:
        if self._config.telemetry_handler is None:
            return
        self._config.telemetry_handler(
            SdkTelemetryEvent(
                method=method.upper(),
                path=path,
                status_code=status_code,
                duration_ms=duration_ms,
                success=success,
                error_type=error_type,
                request_id=request_id,
            )
        )

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
