from __future__ import annotations

from collections.abc import AsyncIterator

from ..exceptions import ValidationError
from ..models.settings import (
    PublicInvitationLookup,
    WorkspaceAccessRequest,
    WorkspaceAccessRequestsPage,
    WorkspaceInvitation,
    WorkspaceInvitations,
    WorkspaceMember,
    WorkspaceMembersPage,
    WorkspaceMutationResult,
    WorkspaceSettings,
)
from .base import AsyncBaseResource


class AsyncSettingsResource(AsyncBaseResource):
    async def workspace(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceSettings:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = await self.http_client.request("GET", "/v1/settings/workspace", auth=auth)
        return WorkspaceSettings.from_dict(dict(data))

    async def create_access_request(
        self,
        *,
        target_tenant_id: str,
        message: str | None = None,
        resend: bool | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        auth = self.build_auth(bearer_token=bearer_token)
        self.require_bearer_token(self.http_client.default_auth.merged_with(auth))
        payload = {"tenant_id": target_tenant_id, "message": message, "resend": resend}
        data = await self.http_client.request(
            "POST",
            "/v1/settings/access-requests",
            json_body={key: value for key, value in payload.items() if value is not None},
            auth=auth,
        )
        return WorkspaceMutationResult.from_dict(dict(data))

    async def invitations(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> WorkspaceInvitations:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = await self.http_client.request(
            "GET",
            "/v1/settings/invitations",
            params=self._build_pagination_params(limit=limit, cursor=cursor),
            auth=auth,
        )
        return WorkspaceInvitations.from_dict(dict(data))

    async def members(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> WorkspaceMembersPage:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = await self.http_client.request(
            "GET",
            "/v1/settings/members",
            params=self._build_pagination_params(limit=limit, cursor=cursor),
            auth=auth,
        )
        return WorkspaceMembersPage.from_dict(dict(data))

    async def iter_all_members(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        page_size: int = 100,
    ) -> AsyncIterator[WorkspaceMember]:
        cursor: str | None = None
        while True:
            page = await self.members(
                tenant_id=tenant_id,
                bearer_token=bearer_token,
                limit=page_size,
                cursor=cursor,
            )
            for item in page.items:
                yield item
            if not page.has_more or page.next_cursor is None:
                return
            cursor = page.next_cursor

    async def access_requests(
        self,
        *,
        scope: str = "my",
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> WorkspaceAccessRequestsPage:
        if scope not in {"my", "workspace"}:
            raise ValidationError("scope must be either 'my' or 'workspace'.")
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        merged_auth = self.http_client.default_auth.merged_with(auth)
        if scope == "workspace":
            self.require_tenant_scope(merged_auth)
        else:
            self.require_bearer_token(merged_auth)
        params = self._build_pagination_params(limit=limit, cursor=cursor) or {}
        params["scope"] = scope
        data = await self.http_client.request(
            "GET",
            "/v1/settings/access-requests",
            params=params,
            auth=auth,
        )
        return WorkspaceAccessRequestsPage.from_dict(dict(data))

    async def iter_all_access_requests(
        self,
        *,
        scope: str = "my",
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        page_size: int = 100,
    ) -> AsyncIterator[WorkspaceAccessRequest]:
        cursor: str | None = None
        while True:
            page = await self.access_requests(
                scope=scope,
                tenant_id=tenant_id,
                bearer_token=bearer_token,
                limit=page_size,
                cursor=cursor,
            )
            for item in page.items:
                yield item
            if not page.has_more or page.next_cursor is None:
                return
            cursor = page.next_cursor

    async def resolve_invitation(
        self,
        *,
        token: str,
    ) -> PublicInvitationLookup:
        if not token.strip():
            raise ValidationError("token must not be empty.")
        data = await self.http_client.request(
            "GET",
            "/v1/public/invitations",
            params={"token": token},
        )
        return PublicInvitationLookup.from_dict(dict(data))

    async def iter_all_invitations(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
        page_size: int = 100,
    ) -> AsyncIterator[WorkspaceInvitation]:
        cursor: str | None = None
        while True:
            page = await self.invitations(
                tenant_id=tenant_id,
                bearer_token=bearer_token,
                limit=page_size,
                cursor=cursor,
            )
            for item in page.items:
                yield item
            if not page.has_more or page.next_cursor is None:
                return
            cursor = page.next_cursor

    async def invite_member(
        self,
        *,
        email: str,
        role: str,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = await self.http_client.request(
            "POST",
            "/v1/settings/invitations",
            json_body={"email": email, "role": role},
            auth=auth,
        )
        return WorkspaceMutationResult.from_dict(dict(data))

    async def manage_invitation(
        self,
        *,
        invitation_id: str,
        action: str,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        return await self._tenant_mutation(
            "/v1/settings/invitations/manage",
            {"invitation_id": invitation_id, "action": action},
            tenant_id=tenant_id,
            bearer_token=bearer_token,
        )

    async def decide_access_request(
        self,
        *,
        request_id: str,
        action: str,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        return await self._tenant_mutation(
            "/v1/settings/access-requests/decision",
            {"request_id": request_id, "action": action},
            tenant_id=tenant_id,
            bearer_token=bearer_token,
        )

    async def manage_membership(
        self,
        *,
        email: str,
        action: str,
        role: str | None = None,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        payload = {"email": email, "action": action, "role": role}
        return await self._tenant_mutation(
            "/v1/settings/memberships",
            {key: value for key, value in payload.items() if value is not None},
            tenant_id=tenant_id,
            bearer_token=bearer_token,
        )

    async def _tenant_mutation(
        self,
        path: str,
        payload: dict[str, object],
        *,
        tenant_id: str | None,
        bearer_token: str | None,
    ) -> WorkspaceMutationResult:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = await self.http_client.request("POST", path, json_body=payload, auth=auth)
        return WorkspaceMutationResult.from_dict(dict(data))

    @staticmethod
    def _build_pagination_params(
        *,
        limit: int | None,
        cursor: str | None,
    ) -> dict[str, str] | None:
        params: dict[str, str] = {}
        if limit is not None:
            if limit < 1 or limit > 100:
                raise ValidationError("limit must be between 1 and 100.")
            params["limit"] = str(limit)
        if cursor is not None:
            if not cursor.strip():
                raise ValidationError("cursor must not be empty.")
            params["cursor"] = cursor
        return params or None
