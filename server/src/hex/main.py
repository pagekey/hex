from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hex.routes.sessions import router as sessions_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)


@app.get("/")
def index():
    return "Hello from server!"
