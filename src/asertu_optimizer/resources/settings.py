from __future__ import annotations

from ..models.settings import (
    WorkspaceInvitations,
    WorkspaceMutationResult,
    WorkspaceSettings,
)
from .base import BaseResource


class SettingsResource(BaseResource):
    def workspace(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceSettings:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = self.http_client.request("GET", "/v1/settings/workspace", auth=auth)
        return WorkspaceSettings.from_dict(dict(data))

    def create_access_request(
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
        data = self.http_client.request(
            "POST",
            "/v1/settings/access-requests",
            json_body={key: value for key, value in payload.items() if value is not None},
            auth=auth,
        )
        return WorkspaceMutationResult.from_dict(dict(data))

    def invitations(
        self,
        *,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceInvitations:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = self.http_client.request("GET", "/v1/settings/invitations", auth=auth)
        return WorkspaceInvitations.from_dict(dict(data))

    def invite_member(
        self,
        *,
        email: str,
        role: str,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = self.http_client.request(
            "POST",
            "/v1/settings/invitations",
            json_body={"email": email, "role": role},
            auth=auth,
        )
        return WorkspaceMutationResult.from_dict(dict(data))

    def manage_invitation(
        self,
        *,
        invitation_id: str,
        action: str,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        return self._tenant_mutation(
            "/v1/settings/invitations/manage",
            {"invitation_id": invitation_id, "action": action},
            tenant_id=tenant_id,
            bearer_token=bearer_token,
        )

    def decide_access_request(
        self,
        *,
        request_id: str,
        action: str,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        return self._tenant_mutation(
            "/v1/settings/access-requests/decision",
            {"request_id": request_id, "action": action},
            tenant_id=tenant_id,
            bearer_token=bearer_token,
        )

    def manage_membership(
        self,
        *,
        email: str,
        action: str,
        role: str | None = None,
        tenant_id: str | None = None,
        bearer_token: str | None = None,
    ) -> WorkspaceMutationResult:
        payload = {"email": email, "action": action, "role": role}
        return self._tenant_mutation(
            "/v1/settings/memberships",
            {key: value for key, value in payload.items() if value is not None},
            tenant_id=tenant_id,
            bearer_token=bearer_token,
        )

    def _tenant_mutation(
        self,
        path: str,
        payload: dict[str, object],
        *,
        tenant_id: str | None,
        bearer_token: str | None,
    ) -> WorkspaceMutationResult:
        auth = self.build_auth(bearer_token=bearer_token, tenant_id=tenant_id)
        self.require_tenant_scope(self.http_client.default_auth.merged_with(auth))
        data = self.http_client.request("POST", path, json_body=payload, auth=auth)
        return WorkspaceMutationResult.from_dict(dict(data))
