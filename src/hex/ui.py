# Copyright 2026 PageKey Solutions, LLC

import os
from pathlib import Path

from fastapi.staticfiles import StaticFiles
import uvicorn

from hex import __version__
from fastapi import FastAPI

app = FastAPI(title="Hex Dev UI")


@app.get("/api/version")
async def version():
    return __version__


current_dir = Path(__file__).parent
ui_static_dir = current_dir / "ui_static"
if ui_static_dir.exists():
    app.mount("/", StaticFiles(directory=str(ui_static_dir), html=True), name="ui")


def run_ui():
    uvicorn.run(
        "hex.ui:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )
