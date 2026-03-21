from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import Settings
from app.schemas.resources import DiscoveryStatus


class ExternalMcpOperationError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class DiscoveryService:
    SKILL_SUBDIRS = ("skills", "commands", "prompts/skills")
    MCP_SUBDIRS = ("mcps", "mcp", "models", "config/mcps")
    CODEX_SKILL_GLOB = "skills/**/SKILL.md"
    MCP_NAME_KEYS = ("name", "title", "display_name", "displayName")
    MCP_MODEL_KEYS = ("model_name", "modelName", "model", "engine")
    MCP_DESCRIPTION_KEYS = ("description",)
    MCP_TEMPERATURE_KEYS = ("temperature",)
    MCP_MAX_TOKENS_KEYS = ("max_tokens", "maxTokens")
    MCP_TOP_P_KEYS = ("top_p", "topP")
    MCP_PRESENCE_PENALTY_KEYS = ("presence_penalty", "presencePenalty")
    MCP_FREQUENCY_PENALTY_KEYS = ("frequency_penalty", "frequencyPenalty")
    MCP_EXTRA_CONTAINER_KEYS = ("extra_params", "extraParams", "parameters")
    GENERIC_SKILL_EXTENSIONS = {
        "",
        ".bash",
        ".json",
        ".md",
        ".markdown",
        ".prompt",
        ".py",
        ".sh",
        ".text",
        ".toml",
        ".txt",
        ".yaml",
        ".yml",
        ".zsh",
    }
    EXTENSION_LANGUAGE_MAP = {
        ".bash": "bash",
        ".json": "json",
        ".md": "markdown",
        ".markdown": "markdown",
        ".prompt": "markdown",
        ".py": "python",
        ".sh": "bash",
        ".text": "text",
        ".toml": "toml",
        ".txt": "text",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".zsh": "bash",
    }

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._ensure_managed_dirs()

    def scan(self) -> list[DiscoveryStatus]:
        return [self._scan_tool(tool, roots) for tool, roots in self.settings.candidate_roots.items()]

    def merge_skills(self, managed_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        combined: dict[str, dict[str, Any]] = {str(item["id"]): item for item in managed_items}
        for item in self.discovered_skills():
            combined.setdefault(str(item["id"]), item)
        return sorted(combined.values(), key=lambda item: str(item.get("updated_at", "")), reverse=True)

    def merge_mcps(self, managed_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        combined: dict[str, dict[str, Any]] = {str(item["id"]): item for item in managed_items}
        for item in self.discovered_mcps():
            combined.setdefault(str(item["id"]), item)
        return sorted(combined.values(), key=lambda item: str(item.get("updated_at", "")), reverse=True)

    def discovered_skills(self) -> list[dict[str, Any]]:
        records: dict[str, dict[str, Any]] = {}
        for tool, roots in self.settings.candidate_roots.items():
            for root in roots:
                if not root.exists():
                    continue
                for record in self._discover_tool_skills(tool, root):
                    records.setdefault(str(record["id"]), record)
        return sorted(records.values(), key=lambda item: str(item.get("updated_at", "")), reverse=True)

    def discovered_skill(self, skill_id: str) -> dict[str, Any] | None:
        return next((item for item in self.discovered_skills() if item.get("id") == skill_id), None)

    def discovered_mcps(self) -> list[dict[str, Any]]:
        records: dict[str, dict[str, Any]] = {}
        for tool, roots in self.settings.candidate_roots.items():
            for root in roots:
                if not root.exists():
                    continue
                for record in self._discover_tool_mcps(tool, root):
                    records.setdefault(str(record["id"]), record)
        return sorted(records.values(), key=lambda item: str(item.get("updated_at", "")), reverse=True)

    def discovered_mcp(self, mcp_id: str) -> dict[str, Any] | None:
        return next((item for item in self.discovered_mcps() if item.get("id") == mcp_id), None)

    def create_discovered_mcp(self, payload: dict[str, Any]) -> dict[str, Any]:
        tool = str(payload.get("cli_tool", ""))
        target_path = self.preview_discovered_mcp_path(tool, payload)
        if target_path.exists():
            raise ExternalMcpOperationError(
                "mcp_conflict",
                f"外部 MCP 文件 '{target_path.name}' 已存在，请修改名称或自定义 ID。",
            )

        serialized = self._serialize_discovered_mcp_payload(payload)
        self._write_mcp_json(target_path, serialized)
        return self._load_discovered_mcp_record(tool, target_path)

    def preview_discovered_mcp_id(self, tool: str, payload: dict[str, Any]) -> str:
        target_path = self.preview_discovered_mcp_path(tool, payload)
        root = self._preferred_external_mcp_dir(tool).parent
        relative_path = target_path.relative_to(root)
        return self._generic_discovered_mcp_id(tool, relative_path)

    def preview_discovered_mcp_path(self, tool: str, payload: dict[str, Any]) -> Path:
        base_dir = self._preferred_external_mcp_dir(tool)
        file_slug = self._slugify(str(payload.get("id") or payload.get("name") or "mcp"))
        return base_dir / f"{file_slug}.json"

    def update_discovered_mcp(self, mcp_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        record = self.discovered_mcp(mcp_id)
        if record is None:
            return None
        if not bool(record.get("is_writable")):
            raise ExternalMcpOperationError("mcp_read_only", f"MCP '{mcp_id}' 来自只读来源，当前不允许修改。")

        source_path = Path(str(record["source_path"])).expanduser().resolve()
        existing_payload = record.get("_raw_payload")
        serialized = self._serialize_discovered_mcp_payload(payload, existing_payload if isinstance(existing_payload, dict) else {})
        self._write_mcp_json(source_path, serialized)
        return self._load_discovered_mcp_record(str(record["cli_tool"]), source_path)

    def delete_discovered_mcp(self, mcp_id: str) -> bool:
        record = self.discovered_mcp(mcp_id)
        if record is None:
            return False
        if not bool(record.get("is_writable")):
            raise ExternalMcpOperationError("mcp_read_only", f"MCP '{mcp_id}' 来自只读来源，当前不允许删除。")

        source_path = Path(str(record["source_path"])).expanduser().resolve()
        try:
            source_path.unlink()
        except FileNotFoundError:
            return False
        except OSError as exc:
            raise ExternalMcpOperationError("mcp_write_failed", f"删除外部 MCP 文件失败：{exc}") from exc
        return True

    def count_skills_by(self, managed_items: list[dict[str, Any]], key: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.merge_skills(managed_items):
            value = str(item.get(key, "unknown"))
            counts[value] = counts.get(value, 0) + 1
        return counts

    def count_mcps_by(self, managed_items: list[dict[str, Any]], key: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.merge_mcps(managed_items):
            value = str(item.get(key, "unknown"))
            counts[value] = counts.get(value, 0) + 1
        return counts

    def _scan_tool(self, tool: str, roots: list[Path]) -> DiscoveryStatus:
        checked = [str(path) for path in roots]
        existing = [path for path in roots if path.exists()]
        managed_skill_path = self.settings.managed_skill_dir / tool
        managed_mcp_path = self.settings.managed_mcp_dir / tool

        if not existing:
            return DiscoveryStatus(
                tool=tool,
                status="missing",
                checked_paths=checked,
                existing_paths=[],
                managed_skill_path=str(managed_skill_path),
                managed_mcp_path=str(managed_mcp_path),
                discovered_skill_files=0,
                discovered_mcp_files=0,
                message="No external configuration directory was found. Managed storage remains available.",
            )

        skill_count = sum(len(self._discover_tool_skills(tool, root)) for root in existing)
        mcp_count = sum(len(self._discover_tool_mcps(tool, root)) for root in existing)
        message = "External directories were found and scanned with best-effort skill parsing plus JSON discovery."
        if tool == "codex":
            message = "External directories were found and scanned with Codex SKILL.md parsing plus best-effort JSON discovery."
        return DiscoveryStatus(
            tool=tool,
            status="available",
            checked_paths=checked,
            existing_paths=[str(path) for path in existing],
            managed_skill_path=str(managed_skill_path),
            managed_mcp_path=str(managed_mcp_path),
            discovered_skill_files=skill_count,
            discovered_mcp_files=mcp_count,
            message=message,
        )

    def _discover_tool_skills(self, tool: str, root: Path) -> list[dict[str, Any]]:
        if tool == "codex":
            return [
                record
                for skill_path in sorted(root.glob(self.CODEX_SKILL_GLOB))
                if (record := self._parse_codex_skill(skill_path, root)) is not None
            ]

        return [
            record
            for skill_path in self._iter_generic_skill_files(root)
            if (record := self._parse_generic_skill(skill_path, root, tool)) is not None
        ]

    def _discover_tool_mcps(self, tool: str, root: Path) -> list[dict[str, Any]]:
        return [
            record
            for mcp_path in self._iter_mcp_files(root)
            if (record := self._parse_generic_mcp(mcp_path, root, tool)) is not None
        ]

    def _iter_generic_skill_files(self, root: Path) -> list[Path]:
        seen: set[Path] = set()
        files: list[Path] = []
        for candidate in self.SKILL_SUBDIRS:
            candidate_path = root / candidate
            if not candidate_path.exists():
                continue
            for path in sorted(candidate_path.rglob("*")):
                if not path.is_file() or path in seen:
                    continue
                if path.name.startswith("."):
                    continue
                if path.suffix.lower() not in self.GENERIC_SKILL_EXTENSIONS:
                    continue
                seen.add(path)
                files.append(path)
        return files

    def _iter_mcp_files(self, root: Path) -> list[Path]:
        seen: set[Path] = set()
        files: list[Path] = []
        for candidate in self.MCP_SUBDIRS:
            candidate_path = root / candidate
            if not candidate_path.exists():
                continue
            for path in sorted(candidate_path.rglob("*.json")):
                if not path.is_file() or path in seen:
                    continue
                if path.name.startswith("."):
                    continue
                seen.add(path)
                files.append(path)
        return files

    def _parse_codex_skill(self, skill_path: Path, root: Path) -> dict[str, Any] | None:
        try:
            raw_text = skill_path.read_text(encoding="utf-8")
        except OSError:
            return None

        metadata_text, body = self._split_front_matter(raw_text)
        metadata = self._parse_front_matter(metadata_text)
        name = metadata.get("name") or skill_path.parent.name
        relative_parent = skill_path.parent.relative_to(root / "skills")
        timestamp = self._path_timestamp(skill_path)
        return {
            "id": self._discovered_skill_id(relative_parent),
            "name": name,
            "description": metadata.get("description", ""),
            "cli_tool": "codex",
            "source_kind": "discovered",
            "source_path": str(skill_path),
            "is_writable": False,
            "created_at": timestamp,
            "updated_at": timestamp,
            "trigger_command": metadata.get("trigger_command") or f"/{name}",
            "script_content": body or raw_text.strip(),
            "script_language": "markdown",
            "tags": [],
        }

    def _parse_generic_skill(self, skill_path: Path, root: Path, tool: str) -> dict[str, Any] | None:
        try:
            raw_text = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None

        metadata_text, body = self._split_front_matter(raw_text)
        metadata = self._parse_front_matter(metadata_text)
        script_content = body or raw_text.strip()
        tags = self._normalize_tags(metadata.get("tags"))

        if skill_path.suffix.lower() == ".json":
            json_metadata, script_content, tags = self._parse_json_skill(raw_text, metadata, tags)
            metadata.update(json_metadata)

        relative_path = skill_path.relative_to(root)
        timestamp = self._path_timestamp(skill_path)
        return {
            "id": self._generic_discovered_skill_id(tool, relative_path),
            "name": metadata.get("name") or metadata.get("title") or self._humanize_name(skill_path.stem or skill_path.name),
            "description": metadata.get("description") or self._infer_description(script_content),
            "cli_tool": tool,
            "source_kind": "discovered",
            "source_path": str(skill_path),
            "is_writable": False,
            "created_at": timestamp,
            "updated_at": timestamp,
            "trigger_command": self._infer_trigger_command(skill_path, metadata),
            "script_content": script_content,
            "script_language": self._infer_script_language(skill_path, metadata),
            "tags": tags,
        }

    def _split_front_matter(self, text: str) -> tuple[str, str]:
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return "", text.strip()

        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                metadata = "\n".join(lines[1:index])
                body = "\n".join(lines[index + 1 :]).strip()
                return metadata, body
        return "", text.strip()

    def _parse_front_matter(self, metadata_text: str) -> dict[str, str]:
        metadata: dict[str, str] = {}
        for line in metadata_text.splitlines():
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line.strip())
            if not match:
                continue
            key, value = match.groups()
            metadata[key] = value.strip().strip("\"'")
        return metadata

    def _discovered_skill_id(self, relative_parent: Path) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(relative_parent).strip().lower()).strip("-")
        return f"codex-discovered-{slug or 'skill'}"

    def _generic_discovered_skill_id(self, tool: str, relative_path: Path) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(relative_path.with_suffix("")).strip().lower()).strip("-")
        return f"{tool}-discovered-{slug or 'skill'}"

    def _generic_discovered_mcp_id(self, tool: str, relative_path: Path) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(relative_path.with_suffix("")).strip().lower()).strip("-")
        return f"{tool}-discovered-{slug or 'mcp'}"

    def _parse_generic_mcp(self, mcp_path: Path, root: Path, tool: str) -> dict[str, Any] | None:
        try:
            payload = json.loads(mcp_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return None

        if not isinstance(payload, dict):
            return None

        relative_path = mcp_path.relative_to(root)
        timestamp = self._path_timestamp(mcp_path)
        model_name = self._first_string(payload, "model_name", "modelName", "model", "engine") or mcp_path.stem
        description = self._first_string(payload, "description") or f"Discovered MCP from {relative_path}"
        return {
            "id": self._generic_discovered_mcp_id(tool, relative_path),
            "name": self._first_string(payload, "name", "title", "display_name", "displayName")
            or self._humanize_name(mcp_path.stem or mcp_path.name),
            "description": description,
            "cli_tool": tool,
            "source_kind": "discovered",
            "source_path": str(mcp_path),
            "is_writable": self._is_writable_discovered_mcp(tool, mcp_path),
            "created_at": timestamp,
            "updated_at": timestamp,
            "model_name": model_name,
            "temperature": self._float_value(payload, "temperature", default=0.2),
            "max_tokens": self._int_value(payload, "max_tokens", "maxTokens", default=2048),
            "top_p": self._float_value(payload, "top_p", "topP", default=1.0),
            "presence_penalty": self._float_value(payload, "presence_penalty", "presencePenalty", default=0.0),
            "frequency_penalty": self._float_value(payload, "frequency_penalty", "frequencyPenalty", default=0.0),
            "extra_params": self._extra_mcp_params(payload),
            "_raw_payload": payload,
        }

    def _parse_json_skill(
        self, raw_text: str, metadata: dict[str, str], existing_tags: list[str]
    ) -> tuple[dict[str, str], str, list[str]]:
        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError:
            return {}, raw_text.strip(), existing_tags

        if not isinstance(payload, dict):
            return {}, raw_text.strip(), existing_tags

        json_metadata: dict[str, str] = {}
        for source_key, target_key in (
            ("name", "name"),
            ("title", "title"),
            ("description", "description"),
            ("trigger_command", "trigger_command"),
            ("trigger", "trigger"),
            ("command", "command"),
            ("script_language", "script_language"),
            ("language", "language"),
        ):
            value = payload.get(source_key)
            if isinstance(value, str) and value.strip():
                json_metadata[target_key] = value.strip()

        script_content = ""
        for key in ("script_content", "script", "content", "prompt", "template", "body", "text"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                script_content = value.strip()
                break

        if not script_content:
            script_content = json.dumps(payload, ensure_ascii=False, indent=2)

        tags = self._normalize_tags(metadata.get("tags")) or self._normalize_tags(payload.get("tags")) or existing_tags
        return json_metadata, script_content, tags

    def _normalize_tags(self, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            if not value.strip():
                return []
            parts = [segment.strip() for segment in re.split(r"[,|/]", value) if segment.strip()]
            return parts or [value.strip()]
        return []

    def _infer_script_language(self, skill_path: Path, metadata: dict[str, str]) -> str:
        for key in ("script_language", "language"):
            value = metadata.get(key)
            if value:
                return value.strip().lower()
        return self.EXTENSION_LANGUAGE_MAP.get(skill_path.suffix.lower(), "text")

    def _infer_trigger_command(self, skill_path: Path, metadata: dict[str, str]) -> str:
        for key in ("trigger_command", "trigger", "command"):
            value = metadata.get(key)
            if value:
                return value.strip()
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", skill_path.stem.strip().lower()).strip("-")
        return f"/{slug or 'skill'}"

    def _humanize_name(self, value: str) -> str:
        text = re.sub(r"[_.-]+", " ", value).strip()
        return text.title() if text else "Discovered Skill"

    def _infer_description(self, script_content: str) -> str:
        for line in script_content.splitlines():
            cleaned = line.strip().lstrip("#").strip()
            if cleaned:
                return cleaned[:120]
        return ""

    def _first_string(self, payload: dict[str, Any], *keys: str) -> str | None:
        for key in keys:
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None

    def _float_value(self, payload: dict[str, Any], *keys: str, default: float) -> float:
        for key in keys:
            value = payload.get(key)
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                try:
                    return float(value.strip())
                except ValueError:
                    continue
        return default

    def _int_value(self, payload: dict[str, Any], *keys: str, default: int) -> int:
        for key in keys:
            value = payload.get(key)
            if isinstance(value, bool):
                continue
            if isinstance(value, int):
                return value
            if isinstance(value, float):
                return int(value)
            if isinstance(value, str):
                try:
                    return int(float(value.strip()))
                except ValueError:
                    continue
        return default

    def _extra_mcp_params(self, payload: dict[str, Any]) -> dict[str, object]:
        recognized = {
            "name",
            "title",
            "display_name",
            "displayName",
            "description",
            "model_name",
            "modelName",
            "model",
            "engine",
            "temperature",
            "max_tokens",
            "maxTokens",
            "top_p",
            "topP",
            "presence_penalty",
            "presencePenalty",
            "frequency_penalty",
            "frequencyPenalty",
            "extra_params",
            "extraParams",
            "parameters",
        }
        extra: dict[str, object] = {}
        for key in ("extra_params", "extraParams", "parameters"):
            value = payload.get(key)
            if isinstance(value, dict):
                extra.update(value)
        for key, value in payload.items():
            if key not in recognized:
                extra[key] = value
        return extra

    def _path_timestamp(self, path: Path) -> str:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).replace(microsecond=0).isoformat()

    def _ensure_managed_dirs(self) -> None:
        for tool in self.settings.candidate_roots:
            (self.settings.managed_skill_dir / tool).mkdir(parents=True, exist_ok=True)
            (self.settings.managed_mcp_dir / tool).mkdir(parents=True, exist_ok=True)

    def _preferred_external_mcp_dir(self, tool: str) -> Path:
        roots = [path.expanduser().resolve() for path in self.settings.candidate_roots.get(tool, []) if path.exists()]
        if not roots:
            raise ExternalMcpOperationError(
                "mcp_external_root_missing",
                f"CLI 工具 '{tool}' 没有可用的外部目录，当前无法创建外部 MCP。",
            )
        target_dir = roots[0] / "mcps"
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir

    def _load_discovered_mcp_record(self, tool: str, path: Path) -> dict[str, Any]:
        root = self._find_matching_root(tool, path)
        if root is None:
            raise ExternalMcpOperationError("mcp_write_failed", f"外部 MCP 路径 '{path}' 不在允许的候选目录下。")
        record = self._parse_generic_mcp(path, root, tool)
        if record is None:
            raise ExternalMcpOperationError("mcp_write_failed", f"外部 MCP 文件 '{path.name}' 不是受支持的 JSON 对象。")
        return record

    def _find_matching_root(self, tool: str, path: Path) -> Path | None:
        resolved_path = path.expanduser().resolve()
        for root in self.settings.candidate_roots.get(tool, []):
            resolved_root = root.expanduser().resolve()
            if not resolved_root.exists():
                continue
            if resolved_path.is_relative_to(resolved_root):
                return resolved_root
        return None

    def _is_writable_discovered_mcp(self, tool: str, path: Path) -> bool:
        resolved_path = path.expanduser().resolve()
        root = self._find_matching_root(tool, resolved_path)
        if root is None or resolved_path.suffix.lower() != ".json":
            return False
        return resolved_path.is_relative_to((root / "mcps").resolve())

    def _serialize_discovered_mcp_payload(
        self,
        payload: dict[str, Any],
        existing_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        current = existing_payload if isinstance(existing_payload, dict) else {}
        result: dict[str, Any] = {}

        self._set_mcp_field(result, current, self.MCP_NAME_KEYS, payload.get("name"))
        self._set_mcp_field(result, current, self.MCP_DESCRIPTION_KEYS, payload.get("description", ""))
        self._set_mcp_field(result, current, self.MCP_MODEL_KEYS, payload.get("model_name"))
        self._set_mcp_field(result, current, self.MCP_TEMPERATURE_KEYS, payload.get("temperature", 0.2))
        self._set_mcp_field(result, current, self.MCP_MAX_TOKENS_KEYS, payload.get("max_tokens", 2048))
        self._set_mcp_field(result, current, self.MCP_TOP_P_KEYS, payload.get("top_p", 1.0))
        self._set_mcp_field(result, current, self.MCP_PRESENCE_PENALTY_KEYS, payload.get("presence_penalty", 0.0))
        self._set_mcp_field(result, current, self.MCP_FREQUENCY_PENALTY_KEYS, payload.get("frequency_penalty", 0.0))

        extra_params = payload.get("extra_params", {})
        if not isinstance(extra_params, dict):
            extra_params = {}

        container_key = next(
            (
                key
                for key in self.MCP_EXTRA_CONTAINER_KEYS
                if key in current and isinstance(current.get(key), dict)
            ),
            None,
        )
        if container_key is not None:
            result[container_key] = extra_params
        else:
            result.update(extra_params)
        return result

    def _set_mcp_field(
        self,
        target: dict[str, Any],
        existing_payload: dict[str, Any],
        aliases: tuple[str, ...],
        value: Any,
    ) -> None:
        key = next((alias for alias in aliases if alias in existing_payload), aliases[0])
        target[key] = value

    def _write_mcp_json(self, path: Path, payload: dict[str, Any]) -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        except OSError as exc:
            raise ExternalMcpOperationError("mcp_write_failed", f"写入外部 MCP 文件失败：{exc}") from exc

    def _slugify(self, value: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
        return cleaned.strip("-") or "mcp"
