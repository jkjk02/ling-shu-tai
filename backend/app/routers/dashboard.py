from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.schemas import DashboardResponse
from app.schemas.resources import ResourceSummary


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(request: Request) -> DashboardResponse:
    services = request.app.state.services
    managed_skills = services["skills"].list()
    managed_mcps = services["mcps"].list()
    all_skills = services["discovery"].merge_skills(managed_skills)
    all_mcps = services["discovery"].merge_mcps(managed_mcps)
    skill_counts = services["discovery"].count_skills_by(managed_skills, "cli_tool")
    mcp_counts = services["discovery"].count_mcps_by(managed_mcps, "cli_tool")
    agent_counts = services["agents"].count_by("cli_tool")

    tool_summaries = []
    for tool in ("codex", "cludea", "opencode"):
        tool_summaries.append(
            ResourceSummary(
                tool=tool,
                skills=skill_counts.get(tool, 0),
                mcps=mcp_counts.get(tool, 0),
                agents=agent_counts.get(tool, 0),
                workflows=len(services["workflows"].list()),
            )
        )

    return DashboardResponse(
        updated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        total_skills=len(all_skills),
        total_mcps=len(all_mcps),
        total_agents=len(services["agents"].list()),
        total_workflows=len(services["workflows"].list()),
        tool_summaries=tool_summaries,
        discovery_summary=services["discovery"].scan(),
    )
