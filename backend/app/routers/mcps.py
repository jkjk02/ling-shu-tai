from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import DeleteResponse, ListResponse, MCP, MCPUpsert
from app.services.discovery import ExternalMcpOperationError
from app.services.resource_service import ResourceConflictError, ResourceLockedError


router = APIRouter(prefix="/mcps", tags=["mcps"])


@router.get("", response_model=ListResponse[MCP])
def list_mcps(request: Request) -> ListResponse[MCP]:
    managed_items = request.app.state.services["mcps"].list()
    items = request.app.state.services["discovery"].merge_mcps(managed_items)
    return ListResponse[MCP](items=[MCP.model_validate(item) for item in items], total=len(items))


@router.get("/{mcp_id}", response_model=MCP)
def get_mcp(mcp_id: str, request: Request) -> MCP:
    item = request.app.state.services["mcps"].get(mcp_id)
    if item is None:
        item = request.app.state.services["discovery"].discovered_mcp(mcp_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"MCP {mcp_id} not found")
    return MCP.model_validate(item)


@router.post("", response_model=MCP, status_code=status.HTTP_201_CREATED)
def create_mcp(payload: MCPUpsert, request: Request) -> MCP:
    payload_data = payload.model_dump()
    mcp_service = request.app.state.services["mcps"]
    discovered_service = request.app.state.services["discovery"]

    if payload.source_kind == "discovered":
        try:
            preview_id = discovered_service.preview_discovered_mcp_id(payload.cli_tool, payload_data)
        except ExternalMcpOperationError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": exc.code,
                    "message": exc.message,
                    "details": {"source_kind": "discovered", "cli_tool": payload.cli_tool},
                },
            ) from exc
        if mcp_service.get(preview_id) is not None or discovered_service.discovered_mcp(preview_id) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "mcp_conflict",
                    "message": f"MCP ID '{preview_id}' 已存在，请修改名称或自定义 ID。",
                    "details": {"id": preview_id},
                },
            )
        try:
            item = discovered_service.create_discovered_mcp(payload_data)
        except ExternalMcpOperationError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": exc.code,
                    "message": exc.message,
                    "details": {"source_kind": "discovered", "cli_tool": payload.cli_tool},
                },
            ) from exc
        return MCP.model_validate(item)

    identifier = mcp_service.resolve_identifier(payload_data)

    if discovered_service.discovered_mcp(identifier) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "mcp_conflict",
                "message": f"MCP ID '{identifier}' 已被外部只读 MCP 占用，请修改名称或自定义 ID。",
                "details": {"id": identifier},
            },
        )

    try:
        item = mcp_service.create_unique(payload_data)
    except ResourceConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "mcp_conflict",
                "message": f"MCP ID '{exc.item_id}' 已存在，请修改名称或自定义 ID。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    return MCP.model_validate(item)


@router.put("/{mcp_id}", response_model=MCP)
def update_mcp(mcp_id: str, payload: MCPUpsert, request: Request) -> MCP:
    discovered_service = request.app.state.services["discovery"]
    discovered_item = discovered_service.discovered_mcp(mcp_id)
    if discovered_item is not None:
        try:
            item = discovered_service.update_discovered_mcp(mcp_id, payload.model_dump())
        except ExternalMcpOperationError as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": exc.code,
                    "message": exc.message,
                    "details": {"id": mcp_id},
                },
            ) from exc
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"MCP {mcp_id} not found")
        return MCP.model_validate(item)
    try:
        item = request.app.state.services["mcps"].update_writable(mcp_id, payload.model_dump())
    except ResourceLockedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "mcp_read_only",
                "message": f"MCP '{exc.item_id}' 来自只读来源，当前不允许修改。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"MCP {mcp_id} not found")
    return MCP.model_validate(item)


@router.delete("/{mcp_id}", response_model=DeleteResponse)
def delete_mcp(mcp_id: str, request: Request) -> DeleteResponse:
    discovered_service = request.app.state.services["discovery"]
    if discovered_service.discovered_mcp(mcp_id) is not None:
        try:
            deleted = discovered_service.delete_discovered_mcp(mcp_id)
        except ExternalMcpOperationError as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": exc.code,
                    "message": exc.message,
                    "details": {"id": mcp_id},
                },
            ) from exc
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"MCP {mcp_id} not found")
        return DeleteResponse(id=mcp_id)
    try:
        deleted = request.app.state.services["mcps"].delete_writable(mcp_id)
    except ResourceLockedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "mcp_read_only",
                "message": f"MCP '{exc.item_id}' 来自只读来源，当前不允许删除。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"MCP {mcp_id} not found")
    return DeleteResponse(id=mcp_id)
