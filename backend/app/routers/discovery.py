from fastapi import APIRouter, Request

from app.schemas.resources import DiscoveryStatus


router = APIRouter(prefix="/discovery", tags=["discovery"])


@router.get("", response_model=list[DiscoveryStatus])
def get_discovery_status(request: Request) -> list[DiscoveryStatus]:
    return request.app.state.services["discovery"].scan()
