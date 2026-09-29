from pathlib import Path

from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from hex.storage import StorageManager
from hex.user import UserManager
from hex.session import SessionManager, InvalidLoginException
from pydantic import BaseModel


router = APIRouter(prefix="/sessions", tags=["sessions"])

storage_manager = StorageManager(
    Path("hexstorage")
)  # TODO figure out how to choose path
user_manager = UserManager(storage_manager)
session_manager = SessionManager(storage_manager, user_manager)


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
            # secure=True,  # TODO uncomment when deploying
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
