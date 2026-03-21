from __future__ import annotations

import json
from pathlib import Path
from typing import Callable


class JsonCollectionRepository:
    def __init__(self, path: Path, seed_factory: Callable[[], list[dict[str, object]]] | None = None) -> None:
        self.path = path
        self.seed_factory = seed_factory or (lambda: [])
        self.ensure_file()

    def ensure_file(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(self.seed_factory())

    def list(self) -> list[dict[str, object]]:
        data = self._read()
        if not isinstance(data, list):
            raise ValueError(f"{self.path} does not contain a JSON list")
        return data

    def get(self, item_id: str) -> dict[str, object] | None:
        return next((item for item in self.list() if item.get("id") == item_id), None)

    def save(self, record: dict[str, object]) -> dict[str, object]:
        items = self.list()
        for index, item in enumerate(items):
            if item.get("id") == record["id"]:
                items[index] = record
                self._write(items)
                return record
        items.append(record)
        self._write(items)
        return record

    def delete(self, item_id: str) -> bool:
        items = self.list()
        filtered = [item for item in items if item.get("id") != item_id]
        if len(filtered) == len(items):
            return False
        self._write(filtered)
        return True

    def _read(self) -> object:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, data: object) -> None:
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
