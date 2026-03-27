from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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
    role: str | None = None

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceSnapshot:
        return cls(
            tenant_id=data.get("tenant_id"),
            name=data.get("name"),
            role=data.get("role"),
        )


@dataclass(frozen=True, slots=True)
class WorkspaceSettings:
    workspace: WorkspaceSnapshot | None = None
    members: list[WorkspaceMember] = field(default_factory=list)
    invitations: list[WorkspaceInvitation] = field(default_factory=list)
    my_access_requests: list[WorkspaceAccessRequest] = field(default_factory=list)
    access_queue: list[WorkspaceAccessRequest] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceSettings:
        workspace_data = data.get("workspace")
        return cls(
            workspace=WorkspaceSnapshot.from_dict(workspace_data)
            if isinstance(workspace_data, dict)
            else None,
            members=[WorkspaceMember.from_dict(item) for item in data.get("members", [])],
            invitations=[
                WorkspaceInvitation.from_dict(item) for item in data.get("invitations", [])
            ],
            my_access_requests=[
                WorkspaceAccessRequest.from_dict(item)
                for item in data.get("my_access_requests", [])
            ],
            access_queue=[
                WorkspaceAccessRequest.from_dict(item) for item in data.get("access_queue", [])
            ],
        )


@dataclass(frozen=True, slots=True)
class WorkspaceInvitations:
    invitations: list[WorkspaceInvitation] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: JsonDict) -> WorkspaceInvitations:
        return cls(
            invitations=[
                WorkspaceInvitation.from_dict(item) for item in data.get("invitations", [])
            ]
        )


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
