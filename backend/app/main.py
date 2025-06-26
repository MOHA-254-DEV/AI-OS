from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import uuid
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Models ----

class User(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatarUrl: str = ""
    registered: str = ""
    lastLogin: str = ""
    status: str = "active"

class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    password: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    password: Optional[str] = None

class AuthResponse(BaseModel):
    user: User
    token: str

class FileEntry(BaseModel):
    name: str
    path: str
    type: str
    size: Optional[int] = 0
    modified: Optional[str] = ""
    previewUrl: Optional[str] = ""

class SystemStats(BaseModel):
    cpuUsage: float
    ramUsage: float
    diskUsage: float
    netUsage: float
    uptime: int
    loadAvg: List[float]

class Process(BaseModel):
    pid: int
    name: str
    user: str
    cpu: float
    mem: float
    started: str
    command: str

class NetworkInterface(BaseModel):
    interface: str
    ip: str
    mac: str
    type: str
    ssid: Optional[str] = None
    status: str
    signalStrength: Optional[int] = None
    speedMbps: Optional[int] = None

class FirewallRule(BaseModel):
    id: str
    name: str
    direction: str
    protocol: str
    port: str
    action: str

class FirewallRuleCreate(BaseModel):
    name: str
    direction: str
    protocol: str
    port: str
    action: str

# ---- Dummy Data ----
USERS = [
    User(
        id="1",
        name="admin",
        email="admin@ai-os.com",
        role="admin",
        avatarUrl="",
        registered="2025-01-01",
        lastLogin="2025-06-01",
        status="active",
    ),
    User(
        id="2",
        name="AI Agent",
        email="agent@ai-os.com",
        role="agent",
        avatarUrl="",
        registered="2025-04-01",
        lastLogin="2025-06-15",
        status="active",
    ),
]
FIREWALL_RULES = []
FILES_ROOT = "./files"
os.makedirs(FILES_ROOT, exist_ok=True)

# ---- Auth Endpoints ----
@app.post("/auth/login", response_model=AuthResponse)
def login(data: dict):
    # Replace with real authentication!
    for user in USERS:
        if user.email == data.get("email"):
            return AuthResponse(user=user, token="dummy-token")
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/auth/logout")
def logout():
    return {"message": "Logged out"}

# ---- User Endpoints ----
@app.get("/users", response_model=List[User])
def list_users():
    return USERS

@app.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    u = User(
        id=str(uuid.uuid4()), name=user.name, email=user.email, role=user.role,
        status="active",
    )
    USERS.append(u)
    return u

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate):
    for u in USERS:
        if u.id == user_id:
            u.name = user.name or u.name
            u.email = user.email or u.email
            u.role = user.role or u.role
            u.status = user.status or u.status
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str):
    global USERS
    USERS = [u for u in USERS if u.id != user_id]
    return

# ---- System Endpoints ----
@app.get("/system/stats", response_model=SystemStats)
def get_stats():
    import random, time
    return SystemStats(
        cpuUsage=random.uniform(10, 70),
        ramUsage=random.uniform(20, 80),
        diskUsage=random.uniform(30, 60),
        netUsage=random.uniform(0, 100),
        uptime=int(time.time() % 100000),
        loadAvg=[random.uniform(0, 2) for _ in range(3)],
    )

@app.get("/system/processes", response_model=List[Process])
def get_processes():
    # Dummy data; hook to psutil or OS API for real values
    return [
        Process(
            pid=1000+i,
            name=f"proc{i}",
            user="root",
            cpu=1.2+i,
            mem=0.8+i,
            started="2025-06-25T10:00:00",
            command=f"/usr/bin/proc{i}",
        ) for i in range(5)
    ]

@app.post("/system/update")
def run_update():
    return {"result": "System updated successfully."}

# ---- Files Endpoints ----
@app.get("/files", response_model=List[FileEntry])
def list_files(path: str = "Home"):
    target = os.path.join(FILES_ROOT, path)
    if not os.path.exists(target):
        os.makedirs(target)
    result = []
    for name in os.listdir(target):
        full = os.path.join(target, name)
        stat = os.stat(full)
        is_dir = os.path.isdir(full)
        result.append(
            FileEntry(
                name=name,
                path=os.path.relpath(full, FILES_ROOT),
                type="folder" if is_dir else "file",
                size=0 if is_dir else stat.st_size,
                modified="",
                previewUrl=None,
            )
        )
    return result

@app.post("/files")
def upload_file(path: str = Form(...), file: UploadFile = File(...)):
    dest_dir = os.path.join(FILES_ROOT, path)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "File uploaded."}

@app.get("/files/{path:path}")
def download_file(path: str):
    target = os.path.join(FILES_ROOT, path)
    if not os.path.isfile(target):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(target)

@app.delete("/files/{path:path}", status_code=204)
def delete_file(path: str):
    target = os.path.join(FILES_ROOT, path)
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="Not found")
    if os.path.isdir(target):
        shutil.rmtree(target)
    else:
        os.remove(target)
    return

# ---- Network Endpoints ----
@app.get("/network/interfaces", response_model=List[NetworkInterface])
def get_interfaces():
    # Dummy; replace with netifaces/psutil for real
    return [
        NetworkInterface(
            interface="eth0",
            ip="192.168.1.10",
            mac="00:11:22:33:44:55",
            type="ethernet",
            status="connected",
            ssid=None,
            signalStrength=None,
            speedMbps=1000,
        ),
        NetworkInterface(
            interface="wlan0",
            ip="192.168.1.11",
            mac="00:11:22:33:44:56",
            type="wifi",
            ssid="AI-OS",
            status="disconnected",
            signalStrength=72,
            speedMbps=150,
        ),
    ]

@app.post("/network/connect")
def connect_network(data: dict):
    return {"result": f"Connected to {data['interface']}"}

@app.post("/network/disconnect")
def disconnect_network(data: dict):
    return {"result": f"Disconnected from {data['interface']}"}

@app.get("/network/firewall", response_model=List[FirewallRule])
def get_firewall_rules():
    return FIREWALL_RULES

@app.post("/network/firewall", response_model=FirewallRule, status_code=201)
def add_firewall_rule(rule: FirewallRuleCreate):
    r = FirewallRule(id=str(uuid.uuid4()), **rule.dict())
    FIREWALL_RULES.append(r)
    return r

@app.delete("/network/firewall/{rule_id}", status_code=204)
def delete_firewall_rule(rule_id: str):
    global FIREWALL_RULES
    FIREWALL_RULES = [r for r in FIREWALL_RULES if r.id != rule_id]
    return

# ---- Terminal Endpoint ----
@app.post("/terminal/run")
def run_terminal(cmd: dict):
    c = cmd.get("command", "")
    # For demo, only safe echo
    if c.strip() == "whoami":
        return {"output": "ai-agent", "code": 0}
    if c.strip() == "time":
        import datetime
        return {"output": str(datetime.datetime.now()), "code": 0}
    if c.strip().startswith("echo "):
        return {"output": c.strip()[5:], "code": 0}
    if c.strip() == "clear":
        return {"output": "", "code": 0}
    if c.strip() == "help":
        return {"output": "Available commands: whoami, time, echo <msg>, clear, help", "code": 0}
    return {"output": f"Command not found: {c}", "code": 127}
