from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


CliTool = Literal["codex", "cludea", "opencode"]
SourceKind = Literal["managed", "discovered"]


class ResourceBase(BaseModel):
    id: str
    name: str
    description: str = ""
    cli_tool: CliTool
    source_kind: SourceKind = "managed"
    source_path: str = ""
    is_writable: bool = True
    created_at: str
    updated_at: str


class Skill(ResourceBase):
    trigger_command: str = ""
    script_content: str = ""
    script_language: str = "markdown"
    tags: list[str] = Field(default_factory=list)


class SkillUpsert(BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    cli_tool: CliTool
    trigger_command: str = ""
    script_content: str = ""
    script_language: str = "markdown"
    tags: list[str] = Field(default_factory=list)
    source_kind: SourceKind = "managed"
    source_path: str = ""
    is_writable: bool = True


class MCP(ResourceBase):
    model_name: str
    temperature: float = 0.2
    max_tokens: int = 2048
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    extra_params: dict[str, object] = Field(default_factory=dict)


class MCPUpsert(BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    cli_tool: CliTool
    model_name: str
    temperature: float = 0.2
    max_tokens: int = 2048
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    extra_params: dict[str, object] = Field(default_factory=dict)
    source_kind: SourceKind = "managed"
    source_path: str = ""
    is_writable: bool = True


class Agent(BaseModel):
    id: str
    name: str
    description: str = ""
    system_prompt: str
    skill_ids: list[str] = Field(default_factory=list)
    mcp_id: str | None = None
    cli_tool: CliTool
    tool_scope: list[CliTool] = Field(default_factory=list)
    created_at: str
    updated_at: str


class AgentUpsert(BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    system_prompt: str
    skill_ids: list[str] = Field(default_factory=list)
    mcp_id: str | None = None
    cli_tool: CliTool
    tool_scope: list[CliTool] = Field(default_factory=list)


class WorkflowNode(BaseModel):
    id: str
    label: str
    agent_id: str | None = None
    position: dict[str, float] = Field(default_factory=dict)
    config: dict[str, object] = Field(default_factory=dict)


class WorkflowEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str = ""
    condition: str | None = None


class Workflow(BaseModel):
    id: str
    name: str
    description: str = ""
    nodes: list[WorkflowNode] = Field(default_factory=list)
    edges: list[WorkflowEdge] = Field(default_factory=list)
    viewport: dict[str, float] = Field(default_factory=dict)
    created_at: str
    updated_at: str


class WorkflowUpsert(BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    nodes: list[WorkflowNode] = Field(default_factory=list)
    edges: list[WorkflowEdge] = Field(default_factory=list)
    viewport: dict[str, float] = Field(default_factory=dict)


class ResourceSummary(BaseModel):
    tool: CliTool
    skills: int = 0
    mcps: int = 0
    agents: int = 0
    workflows: int = 0


class DiscoveryStatus(BaseModel):
    tool: CliTool
    status: Literal["available", "missing", "error"]
    checked_paths: list[str] = Field(default_factory=list)
    existing_paths: list[str] = Field(default_factory=list)
    managed_skill_path: str
    managed_mcp_path: str
    discovered_skill_files: int = 0
    discovered_mcp_files: int = 0
    message: str


class DashboardResponse(BaseModel):
    updated_at: str
    total_skills: int
    total_mcps: int
    total_agents: int
    total_workflows: int
    tool_summaries: list[ResourceSummary]
    discovery_summary: list[DiscoveryStatus]
