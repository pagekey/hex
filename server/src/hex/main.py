import os
import sys
from pathlib import Path


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from hex.routes.sessions import router as sessions_router
from hex.routes.workflows import router as workflows_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)
app.include_router(workflows_router)


@app.get("/")
def index():
    return "Hello from Hex server!"


def get_static_dir() -> Path:
    return Path(__file__).parent / "static"


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        if path == ".":
            path = "index.html"
        full_path, stat_result = self.lookup_path(path)
        if stat_result is None:
            # File not found, serve index.html instead.
            index_path = os.path.join(self.directory, "index.html")
            if os.path.exists(index_path):
                return FileResponse(index_path)
            # Fallback: Raise 404 if index.html also missing
            raise HTTPException(status_code=404)
        return await super().get_response(path, scope)


app.mount("/ui", SPAStaticFiles(directory=get_static_dir()), name="static")
