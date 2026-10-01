from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from hex.globals import (
    session_manager,
    storage_manager,
    user_manager,
)
from hex.session import InvalidLoginException

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.get("")
async def home():
    return "Hello from sessions"


@router.post("/seed")
async def seed():
    if storage_manager.load("users", "admin") is None:
        user_manager.create("admin", "admin123456")
        return "Created admin user"
    else:
        return "Admin user exists already"


class CreateSessionRequest(BaseModel):
    username: str
    password: str


@router.post("")
async def create_session(request: CreateSessionRequest):
    try:
        session_id = session_manager.create_session(request.username, request.password)
        response = JSONResponse(status_code=201, content={"message": "Session created"})
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
            secure=False,  # TODO set to True in prod
            path="/",
        )
        return response
    except InvalidLoginException:
        return JSONResponse(
            status_code=401, content={"message": "Invalid username or password"}
        )


@router.get("/check")
async def check_session(session_id: str | None = Cookie(default=None)):
    if session_id is None:
        return {"authenticated": False}

    username = session_manager.get_session_username(session_id)

    if username is None:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "username": username,
    }


@router.delete("")
def delete_current_session():
    response = JSONResponse(status_code=200, content={"message": "Session deleted"})
    response.set_cookie(
        key="session_id",
        value="",
        httponly=True,
        samesite="lax",
        secure=False,  # TODO set to True in prod
        path="/",
    )
    return response
