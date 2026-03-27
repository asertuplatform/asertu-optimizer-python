from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .tenants import Pagination

JsonDict = dict[str, Any]


@dataclass(frozen=True, slots=True)
class WorkspaceMember:
    email: str | None = None
    role: str | None = None
    status: str | None = None
    is_default: bool | None = None
    created_at: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceMember:
        return cls(**{field: data.get(field) for field in cls.__dataclass_fields__})


@dataclass(frozen=True, slots=True)
class WorkspaceInvitation:
    invitation_id: str | None = None
    email: str | None = None
    role: str | None = None
    status: str | None = None
    expires_at: str | None = None
    invited_by_email: str | None = None
    created_at: str | None = None
    latest_delivery_status: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceInvitation:
        return cls(**{field: data.get(field) for field in cls.__dataclass_fields__})


@dataclass(frozen=True, slots=True)
class WorkspaceAccessRequest:
    request_id: str | None = None
    tenant_id: str | None = None
    tenant_name: str | None = None
    email: str | None = None
    message: str | None = None
    status: str | None = None
    created_at: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceAccessRequest:
        return cls(**{field: data.get(field) for field in cls.__dataclass_fields__})


@dataclass(frozen=True, slots=True)
class WorkspaceSnapshot:
    tenant_id: str | None = None
    name: str | None = None
    plan: str | None = None
    status: str | None = None
    role: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceSnapshot:
        return cls(
            tenant_id=data.get("tenant_id"),
            name=data.get("name"),
            plan=data.get("plan"),
            status=data.get("status"),
            role=data.get("role"),
        )


@dataclass(frozen=True, slots=True)
class WorkspacePermissions:
    can_invite: bool | None = None
    can_manage_requests: bool | None = None
    can_manage_members: bool | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspacePermissions:
        return cls(
            can_invite=data.get("can_invite"),
            can_manage_requests=data.get("can_manage_requests"),
            can_manage_members=data.get("can_manage_members"),
        )


@dataclass(frozen=True, slots=True)
class PublicInvitationWorkspace:
    tenant_id: str | None = None
    workspace_name: str | None = None
    role: str | None = None
    status: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> PublicInvitationWorkspace:
        return cls(
            tenant_id=data.get("tenant_id"),
            workspace_name=data.get("workspace_name"),
            role=data.get("role"),
            status=data.get("status"),
        )


@dataclass(frozen=True, slots=True)
class PublicInvitation:
    token: str | None = None
    tenant_id: str | None = None
    workspace_name: str | None = None
    email: str | None = None
    role: str | None = None
    status: str | None = None
    expires_at: str | None = None
    accepted_at: str | None = None
    revoked_at: str | None = None
    is_expired: bool | None = None
    invited_by_email: str | None = None
    intent_options: list[str] = field(default_factory=list)
    existing_workspaces: list[PublicInvitationWorkspace] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> PublicInvitation:
        return cls(
            token=data.get("token"),
            tenant_id=data.get("tenant_id"),
            workspace_name=data.get("workspace_name"),
            email=data.get("email"),
            role=data.get("role"),
            status=data.get("status"),
            expires_at=data.get("expires_at"),
            accepted_at=data.get("accepted_at"),
            revoked_at=data.get("revoked_at"),
            is_expired=data.get("is_expired"),
            invited_by_email=data.get("invited_by_email"),
            intent_options=list(data.get("intent_options") or []),
            existing_workspaces=[
                PublicInvitationWorkspace.from_dict(item)
                for item in data.get("existing_workspaces", [])
            ],
        )


@dataclass(frozen=True, slots=True)
class PublicInvitationLookup:
    invitation: PublicInvitation | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> PublicInvitationLookup:
        invitation = data.get("invitation")
        return cls(
            invitation=PublicInvitation.from_dict(invitation)
            if isinstance(invitation, dict)
            else None,
        )


@dataclass(frozen=True, slots=True)
class WorkspaceSettings:
    workspace: WorkspaceSnapshot | None = None
    permissions: WorkspacePermissions | None = None
    members: list[WorkspaceMember] = field(default_factory=list)
    invitations: list[WorkspaceInvitation] = field(default_factory=list)
    notifications: list[JsonDict] = field(default_factory=list)
    my_access_requests: list[WorkspaceAccessRequest] = field(default_factory=list)
    access_queue: list[WorkspaceAccessRequest] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceSettings:
        workspace_data = data.get("workspace")
        permissions_data = data.get("permissions")
        return cls(
            workspace=WorkspaceSnapshot.from_dict(workspace_data)
            if isinstance(workspace_data, dict)
            else None,
            permissions=WorkspacePermissions.from_dict(permissions_data)
            if isinstance(permissions_data, dict)
            else None,
            members=[WorkspaceMember.from_dict(item) for item in data.get("members", [])],
            invitations=[
                WorkspaceInvitation.from_dict(item) for item in data.get("invitations", [])
            ],
            notifications=[
                item for item in (data.get("notifications") or []) if isinstance(item, dict)
            ],
            my_access_requests=[
                WorkspaceAccessRequest.from_dict(item)
                for item in (data.get("my_access_requests", data.get("access_requests", [])) or [])
            ],
            access_queue=[
                WorkspaceAccessRequest.from_dict(item)
                for item in (data.get("access_queue", data.get("workspace_requests", [])) or [])
            ],
        )


@dataclass(frozen=True, slots=True)
class WorkspaceMembersPage:
    workspace: WorkspaceSnapshot | None = None
    members: list[WorkspaceMember] = field(default_factory=list)
    pagination: Pagination | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceMembersPage:
        workspace = data.get("workspace")
        pagination = data.get("pagination")
        return cls(
            workspace=(
                WorkspaceSnapshot.from_dict(workspace) if isinstance(workspace, dict) else None
            ),
            members=[WorkspaceMember.from_dict(item) for item in data.get("members", [])],
            pagination=Pagination.from_dict(pagination) if isinstance(pagination, dict) else None,
        )

    @property
    def items(self) -> list[WorkspaceMember]:
        return self.members

    @property
    def next_cursor(self) -> str | None:
        return self.pagination.next_cursor if self.pagination is not None else None

    @property
    def has_more(self) -> bool:
        return self.pagination.has_more if self.pagination is not None else False


@dataclass(frozen=True, slots=True)
class WorkspaceAccessRequestsPage:
    scope: str | None = None
    workspace: WorkspaceSnapshot | None = None
    requests: list[WorkspaceAccessRequest] = field(default_factory=list)
    pagination: Pagination | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceAccessRequestsPage:
        workspace = data.get("workspace")
        pagination = data.get("pagination")
        return cls(
            scope=data.get("scope"),
            workspace=(
                WorkspaceSnapshot.from_dict(workspace) if isinstance(workspace, dict) else None
            ),
            requests=[WorkspaceAccessRequest.from_dict(item) for item in data.get("requests", [])],
            pagination=Pagination.from_dict(pagination) if isinstance(pagination, dict) else None,
        )

    @property
    def items(self) -> list[WorkspaceAccessRequest]:
        return self.requests

    @property
    def next_cursor(self) -> str | None:
        return self.pagination.next_cursor if self.pagination is not None else None

    @property
    def has_more(self) -> bool:
        return self.pagination.has_more if self.pagination is not None else False


@dataclass(frozen=True, slots=True)
class WorkspaceInvitations:
    workspace: WorkspaceSnapshot | None = None
    invitations: list[WorkspaceInvitation] = field(default_factory=list)
    pagination: Pagination | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceInvitations:
        workspace = data.get("workspace")
        pagination = data.get("pagination")
        return cls(
            workspace=(
                WorkspaceSnapshot.from_dict(workspace) if isinstance(workspace, dict) else None
            ),
            invitations=[
                WorkspaceInvitation.from_dict(item) for item in data.get("invitations", [])
            ],
            pagination=Pagination.from_dict(pagination) if isinstance(pagination, dict) else None,
        )

    @property
    def items(self) -> list[WorkspaceInvitation]:
        return self.invitations

    @property
    def next_cursor(self) -> str | None:
        return self.pagination.next_cursor if self.pagination is not None else None

    @property
    def has_more(self) -> bool:
        return self.pagination.has_more if self.pagination is not None else False


@dataclass(frozen=True, slots=True)
class WorkspaceMutationResult:
    message: str | None = None
    invitation_id: str | None = None
    request_id: str | None = None
    status: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceMutationResult:
        return cls(
            message=data.get("message"),
            invitation_id=data.get("invitation_id"),
            request_id=data.get("request_id"),
            status=data.get("status"),
        )
