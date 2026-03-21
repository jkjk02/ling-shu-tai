from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import Agent, AgentUpsert, DeleteResponse, ListResponse
from app.services.resource_service import ResourceConflictError


router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=ListResponse[Agent])
def list_agents(request: Request) -> ListResponse[Agent]:
    items = request.app.state.services["agents"].list()
    return ListResponse[Agent](items=[Agent.model_validate(item) for item in items], total=len(items))


@router.get("/{agent_id}", response_model=Agent)
def get_agent(agent_id: str, request: Request) -> Agent:
    item = request.app.state.services["agents"].get(agent_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Agent {agent_id} not found")
    return Agent.model_validate(item)


@router.post("", response_model=Agent, status_code=status.HTTP_201_CREATED)
def create_agent(payload: AgentUpsert, request: Request) -> Agent:
    try:
        item = request.app.state.services["agents"].create_unique(payload.model_dump())
    except ResourceConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "agent_conflict",
                "message": f"Agent ID '{exc.item_id}' 已存在，请修改名称或自定义 ID。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    return Agent.model_validate(item)


@router.put("/{agent_id}", response_model=Agent)
def update_agent(agent_id: str, payload: AgentUpsert, request: Request) -> Agent:
    item = request.app.state.services["agents"].update(agent_id, payload.model_dump())
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Agent {agent_id} not found")
    return Agent.model_validate(item)


@router.delete("/{agent_id}", response_model=DeleteResponse)
def delete_agent(agent_id: str, request: Request) -> DeleteResponse:
    deleted = request.app.state.services["agents"].delete(agent_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Agent {agent_id} not found")
    return DeleteResponse(id=agent_id)
