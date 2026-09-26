from fastapi import APIRouter


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("")
async def fakeroute():
    return "Hello from sessions"
