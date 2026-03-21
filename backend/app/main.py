from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.repositories import JsonCollectionRepository
from app.routers import build_api_router
from app.services import DiscoveryService, ResourceService


def create_app() -> FastAPI:
    settings = get_settings()
    repositories = {
        "skills": JsonCollectionRepository(settings.collection_files["skills"], _seed_skills),
        "mcps": JsonCollectionRepository(settings.collection_files["mcps"], _seed_mcps),
        "agents": JsonCollectionRepository(settings.collection_files["agents"], _seed_agents),
        "workflows": JsonCollectionRepository(settings.collection_files["workflows"], _seed_workflows),
    }
    services = {
        "skills": ResourceService(repositories["skills"]),
        "mcps": ResourceService(repositories["mcps"]),
        "agents": ResourceService(repositories["agents"]),
        "workflows": ResourceService(repositories["workflows"]),
        "discovery": DiscoveryService(settings),
    }

    app = FastAPI(title=settings.project_name, version="0.1.0")
    app.state.settings = settings
    app.state.repositories = repositories
    app.state.services = services

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict):
            detail = exc.detail
            code = str(detail.get("code") or f"http_{exc.status_code}")
            message = str(detail.get("message") or f"HTTP {exc.status_code}")
            details = detail.get("details")
            normalized_details = details if isinstance(details, dict) else None
        else:
            code = f"http_{exc.status_code}"
            message = str(exc.detail)
            normalized_details = None

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": code,
                    "message": message,
                    "details": normalized_details,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_server_error",
                    "message": "Unexpected backend error.",
                    "details": {"type": exc.__class__.__name__},
                }
            },
        )

    app.include_router(build_api_router(), prefix=settings.api_prefix)
    return app


def _seed_skills() -> list[dict[str, object]]:
    return [
        {
            "id": "codex-skill-bootstrap",
            "name": "Bootstrap Workspace",
            "description": "Prepare a new workspace layout for a Codex task.",
            "cli_tool": "codex",
            "source_kind": "managed",
            "source_path": "backend/data/managed/skills/codex/bootstrap.json",
            "is_writable": True,
            "trigger_command": "/bootstrap",
            "script_content": "Create the folders, read docs, and summarize the plan.",
            "script_language": "markdown",
            "tags": ["setup", "workspace"],
            "created_at": "2026-03-19T00:00:00+00:00",
            "updated_at": "2026-03-19T00:00:00+00:00",
        }
    ]


def _seed_mcps() -> list[dict[str, object]]:
    return [
        {
            "id": "opencode-default-model",
            "name": "Default Model",
            "description": "Baseline model profile for opencode tasks.",
            "cli_tool": "opencode",
            "source_kind": "managed",
            "source_path": "backend/data/managed/mcps/opencode/default.json",
            "is_writable": True,
            "model_name": "gpt-5.4",
            "temperature": 0.2,
            "max_tokens": 8192,
            "top_p": 1.0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "extra_params": {"reasoning_effort": "medium"},
            "created_at": "2026-03-19T00:00:00+00:00",
            "updated_at": "2026-03-19T00:00:00+00:00",
        }
    ]


def _seed_agents() -> list[dict[str, object]]:
    return [
        {
            "id": "planner-agent",
            "name": "Planner Agent",
            "description": "Coordinates implementation steps.",
            "system_prompt": "Break work into staged deliverables and keep handoffs precise.",
            "skill_ids": ["codex-skill-bootstrap"],
            "mcp_id": "opencode-default-model",
            "cli_tool": "codex",
            "tool_scope": ["codex", "opencode"],
            "created_at": "2026-03-19T00:00:00+00:00",
            "updated_at": "2026-03-19T00:00:00+00:00",
        }
    ]


def _seed_workflows() -> list[dict[str, object]]:
    return [
        {
            "id": "draft-delivery-workflow",
            "name": "Draft Delivery Workflow",
            "description": "Simple author-review flow for a managed delivery.",
            "nodes": [
                {
                    "id": "node-1",
                    "label": "Planner",
                    "agent_id": "planner-agent",
                    "position": {"x": 120.0, "y": 80.0},
                    "config": {},
                }
            ],
            "edges": [],
            "viewport": {"x": 0.0, "y": 0.0, "zoom": 1.0},
            "created_at": "2026-03-19T00:00:00+00:00",
            "updated_at": "2026-03-19T00:00:00+00:00",
        }
    ]


app = create_app()
