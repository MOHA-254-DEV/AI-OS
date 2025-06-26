import platform
import subprocess
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.post("/exec", response_model=dict)
def execute_command(
    command: str = Body(..., embed=True),
    current_user=Depends(get_current_active_admin)
):
    try:
        result = subprocess.run(
            command, shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return {"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode}
    except subprocess.CalledProcessError as e:
        return {"stdout": e.stdout or "", "stderr": e.stderr or str(e), "exit_code": e.returncode}
