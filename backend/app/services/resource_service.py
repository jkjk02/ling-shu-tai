from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from app.repositories import JsonCollectionRepository


class ResourceConflictError(Exception):
    def __init__(self, item_id: str) -> None:
        super().__init__(f"Resource {item_id} already exists")
        self.item_id = item_id


class ResourceLockedError(Exception):
    def __init__(self, item_id: str) -> None:
        super().__init__(f"Resource {item_id} is not writable")
        self.item_id = item_id


class ResourceService:
    def __init__(self, repository: JsonCollectionRepository, *, default_cli_tool: str | None = None) -> None:
        self.repository = repository
        self.default_cli_tool = default_cli_tool

    def list(self) -> list[dict[str, Any]]:
        items = self.repository.list()
        return sorted(items, key=lambda item: str(item.get("updated_at", "")), reverse=True)

    def get(self, item_id: str) -> dict[str, Any] | None:
        return self.repository.get(item_id)

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        timestamp = self._timestamp()
        identifier = self.resolve_identifier(payload)
        record = {
            **payload,
            "id": identifier,
            "cli_tool": payload.get("cli_tool", self.default_cli_tool),
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        return self.repository.save(record)

    def create_unique(self, payload: dict[str, Any]) -> dict[str, Any]:
        identifier = self.resolve_identifier(payload)
        if self.repository.get(identifier) is not None:
            raise ResourceConflictError(identifier)
        return self.create({**payload, "id": identifier})

    def resolve_identifier(self, payload: dict[str, Any]) -> str:
        return str(payload.get("id") or self._slugify(str(payload["name"])))

    def update(self, item_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        current = self.repository.get(item_id)
        if current is None:
            return None
        record = {
            **current,
            **payload,
            "id": item_id,
            "created_at": current.get("created_at", self._timestamp()),
            "updated_at": self._timestamp(),
        }
        return self.repository.save(record)

    def update_writable(self, item_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        current = self.repository.get(item_id)
        if current is None:
            return None
        if not bool(current.get("is_writable", True)):
            raise ResourceLockedError(item_id)
        return self.update(item_id, payload)

    def delete(self, item_id: str) -> bool:
        return self.repository.delete(item_id)

    def delete_writable(self, item_id: str) -> bool:
        current = self.repository.get(item_id)
        if current is None:
            return False
        if not bool(current.get("is_writable", True)):
            raise ResourceLockedError(item_id)
        return self.delete(item_id)

    def count_by(self, key: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.repository.list():
            value = str(item.get(key, "unknown"))
            counts[value] = counts.get(value, 0) + 1
        return counts

    def latest_update(self) -> str:
        items = self.list()
        if not items:
            return self._timestamp()
        return str(items[0].get("updated_at", self._timestamp()))

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def _slugify(self, value: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
        return cleaned.strip("-") or "resource"
