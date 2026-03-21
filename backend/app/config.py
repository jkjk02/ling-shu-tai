from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path


CliTool = str


@dataclass(slots=True)
class Settings:
    project_name: str = "Ling Shu Tai API"
    api_prefix: str = "/api"
    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parents[1])
    data_dir: Path = field(init=False)
    collection_files: dict[str, Path] = field(init=False)
    managed_skill_dir: Path = field(init=False)
    managed_mcp_dir: Path = field(init=False)
    agent_dir: Path = field(init=False)
    workflow_dir: Path = field(init=False)
    candidate_roots: dict[CliTool, list[Path]] = field(init=False)

    def __post_init__(self) -> None:
        data_dir_override = os.environ.get("LINGSHU_DATA_DIR")
        if data_dir_override:
            self.data_dir = Path(data_dir_override).expanduser().resolve()
        else:
            self.data_dir = self.base_dir / "data"
        self.collection_files = {
            "skills": self.data_dir / "skills.json",
            "mcps": self.data_dir / "mcps.json",
            "agents": self.data_dir / "agents" / "agents.json",
            "workflows": self.data_dir / "workflows" / "workflows.json",
        }
        self.managed_skill_dir = self.data_dir / "managed" / "skills"
        self.managed_mcp_dir = self.data_dir / "managed" / "mcps"
        self.agent_dir = self.data_dir / "agents"
        self.workflow_dir = self.data_dir / "workflows"
        home = Path(os.environ.get("HOME", str(Path.home()))).expanduser()
        self.candidate_roots = {
            "codex": self._paths_from_env("LINGSHU_CODEX_ROOT", [home / ".codex", home / ".config" / "codex"]),
            "cludea": self._paths_from_env(
                "LINGSHU_CLUDEA_ROOT",
                [
                    home / ".cludea",
                    home / ".config" / "cludea",
                    home / ".claude",
                    home / ".config" / "claude",
                ],
            ),
            "opencode": self._paths_from_env("LINGSHU_OPENCODE_ROOT", [home / ".opencode", home / ".config" / "opencode"]),
        }

    def _paths_from_env(self, env_name: str, fallback: list[Path]) -> list[Path]:
        override = os.environ.get(env_name)
        if not override:
            return fallback
        return [Path(segment).expanduser() for segment in override.split(os.pathsep) if segment]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
