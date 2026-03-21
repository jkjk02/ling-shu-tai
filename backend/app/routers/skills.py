from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import DeleteResponse, ListResponse, Skill, SkillUpsert
from app.services.resource_service import ResourceConflictError, ResourceLockedError


router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=ListResponse[Skill])
def list_skills(request: Request) -> ListResponse[Skill]:
    managed_items = request.app.state.services["skills"].list()
    items = request.app.state.services["discovery"].merge_skills(managed_items)
    return ListResponse[Skill](items=[Skill.model_validate(item) for item in items], total=len(items))


@router.get("/{skill_id}", response_model=Skill)
def get_skill(skill_id: str, request: Request) -> Skill:
    item = request.app.state.services["skills"].get(skill_id)
    if item is None:
        item = request.app.state.services["discovery"].discovered_skill(skill_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Skill {skill_id} not found")
    return Skill.model_validate(item)


@router.post("", response_model=Skill, status_code=status.HTTP_201_CREATED)
def create_skill(payload: SkillUpsert, request: Request) -> Skill:
    payload_data = payload.model_dump()
    skill_service = request.app.state.services["skills"]
    discovered_service = request.app.state.services["discovery"]
    identifier = skill_service.resolve_identifier(payload_data)

    if discovered_service.discovered_skill(identifier) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "skill_conflict",
                "message": f"Skill ID '{identifier}' 已被外部只读 Skill 占用，请修改名称或自定义 ID。",
                "details": {"id": identifier},
            },
        )

    try:
        item = skill_service.create_unique(payload_data)
    except ResourceConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "skill_conflict",
                "message": f"Skill ID '{exc.item_id}' 已存在，请修改名称或自定义 ID。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    return Skill.model_validate(item)


@router.put("/{skill_id}", response_model=Skill)
def update_skill(skill_id: str, payload: SkillUpsert, request: Request) -> Skill:
    if request.app.state.services["discovery"].discovered_skill(skill_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "skill_read_only",
                "message": f"Skill '{skill_id}' 来自只读来源，当前不允许修改。",
                "details": {"id": skill_id},
            },
        )
    try:
        item = request.app.state.services["skills"].update_writable(skill_id, payload.model_dump())
    except ResourceLockedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "skill_read_only",
                "message": f"Skill '{exc.item_id}' 来自只读来源，当前不允许修改。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Skill {skill_id} not found")
    return Skill.model_validate(item)


@router.delete("/{skill_id}", response_model=DeleteResponse)
def delete_skill(skill_id: str, request: Request) -> DeleteResponse:
    if request.app.state.services["discovery"].discovered_skill(skill_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "skill_read_only",
                "message": f"Skill '{skill_id}' 来自只读来源，当前不允许删除。",
                "details": {"id": skill_id},
            },
        )
    try:
        deleted = request.app.state.services["skills"].delete_writable(skill_id)
    except ResourceLockedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "skill_read_only",
                "message": f"Skill '{exc.item_id}' 来自只读来源，当前不允许删除。",
                "details": {"id": exc.item_id},
            },
        ) from exc
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Skill {skill_id} not found")
    return DeleteResponse(id=skill_id)
