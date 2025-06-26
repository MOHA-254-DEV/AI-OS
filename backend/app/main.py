from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api.v1.endpoints import (
    auth, users, files, system, network, terminal
)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS middleware for cross-origin requests, allow all for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(files.router, prefix=f"{settings.API_V1_STR}/files", tags=["files"])
app.include_router(system.router, prefix=f"{settings.API_V1_STR}/system", tags=["system"])
app.include_router(network.router, prefix=f"{settings.API_V1_STR}/network", tags=["network"])
app.include_router(terminal.router, prefix=f"{settings.API_V1_STR}/terminal", tags=["terminal"])

@app.get("/")
def root():
    return {"msg": "AI-OS Backend is running."}
