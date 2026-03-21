from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field


ItemT = TypeVar("ItemT")


class ErrorDetail(BaseModel):
    code: str = Field(description="Stable error code for the frontend.")
    message: str
    details: dict[str, object] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class DeleteResponse(BaseModel):
    deleted: bool = True
    id: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ListResponse(BaseModel, Generic[ItemT]):
    items: list[ItemT]
    total: int
