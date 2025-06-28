from fastapi import FastAPI
from app.api.v1.endpoints import (
    auth, users, organizations, notifications, files, network, firewall, quota, audit_log, legal_hold
)

app = FastAPI(title="AI-OS Backend", version="1.0.0")

# Register routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(organizations.router, prefix="/api/v1/organizations", tags=["organizations"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(network.router, prefix="/api/v1/network", tags=["network"])
app.include_router(firewall.router, prefix="/api/v1/firewall", tags=["firewall"])
app.include_router(quota.router, prefix="/api/v1/quota", tags=["quota"])
app.include_router(audit_log.router, prefix="/api/v1/audit-log", tags=["audit_log"])
app.include_router(legal_hold.router, prefix="/api/v1/legal-hold", tags=["legal_hold"])
