from fastapi import FastAPI

from hex.routes.sessions import router as sessions_router

app = FastAPI()

app.include_router(sessions_router)


@app.get("/")
def index():
    return "Hello from server!"
