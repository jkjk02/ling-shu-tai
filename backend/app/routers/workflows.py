from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import DeleteResponse, ListResponse, Workflow, WorkflowUpsert
from app.services.resource_service import ResourceConflictError


router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("", response_model=ListResponse[Workflow])
def list_workflows(request: Request) -> ListResponse[Workflow]:
    items = request.app.state.services["workflows"].list()
    return ListResponse[Workflow](items=[Workflow.model_validate(item) for item in items], total=len(items))


@router.get("/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: str, request: Request) -> Workflow:
    item = request.app.state.services["workflows"].get(workflow_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workflow {workflow_id} not found")
    return Workflow.model_validate(item)


@router.post("", response_model=Workflow, status_code=status.HTTP_201_CREATED)
def create_workflow(payload: WorkflowUpsert, request: Request) -> Workflow:
    _validate_workflow_payload(payload, request)
    try:
        item = request.app.state.services["workflows"].create_unique(payload.model_dump())
    except ResourceConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "workflow_conflict",
                "message": f"Workflow ID '{exc.item_id}' 已存在，请修改名称或自定义 ID。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    return Workflow.model_validate(item)


@router.put("/{workflow_id}", response_model=Workflow)
def update_workflow(workflow_id: str, payload: WorkflowUpsert, request: Request) -> Workflow:
    _validate_workflow_payload(payload, request)
    item = request.app.state.services["workflows"].update(workflow_id, payload.model_dump())
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workflow {workflow_id} not found")
    return Workflow.model_validate(item)


@router.delete("/{workflow_id}", response_model=DeleteResponse)
def delete_workflow(workflow_id: str, request: Request) -> DeleteResponse:
    deleted = request.app.state.services["workflows"].delete(workflow_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workflow {workflow_id} not found")
    return DeleteResponse(id=workflow_id)


def _validate_workflow_payload(payload: WorkflowUpsert, request: Request) -> None:
    node_ids = [node.id for node in payload.nodes]
    duplicate_node_ids = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
    if duplicate_node_ids:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "workflow_invalid",
                "message": "Workflow 中存在重复节点 ID。",
                "details": {"duplicate_node_ids": duplicate_node_ids},
            },
        )

    edge_ids = [edge.id for edge in payload.edges]
    duplicate_edge_ids = sorted({edge_id for edge_id in edge_ids if edge_ids.count(edge_id) > 1})
    if duplicate_edge_ids:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "workflow_invalid",
                "message": "Workflow 中存在重复连线 ID。",
                "details": {"duplicate_edge_ids": duplicate_edge_ids},
            },
        )

    node_id_set = set(node_ids)
    invalid_edges = [
        edge.id
        for edge in payload.edges
        if edge.source not in node_id_set or edge.target not in node_id_set or edge.source == edge.target
    ]
    if invalid_edges:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "workflow_invalid",
                "message": "Workflow 中存在无效连线，起点或终点缺失，或出现自连线。",
                "details": {"invalid_edge_ids": invalid_edges},
            },
        )

    agent_ids = {agent["id"] for agent in request.app.state.services["agents"].list()}
    invalid_node_agents = sorted(
        node.id for node in payload.nodes if node.agent_id is not None and node.agent_id not in agent_ids
    )
    if invalid_node_agents:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "workflow_invalid",
                "message": "Workflow 中存在引用不存在 Agent 的节点。",
                "details": {"invalid_node_agent_ids": invalid_node_agents},
            },
        )
