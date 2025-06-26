import platform
import psutil
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_active_admin
import subprocess

router = APIRouter()

@router.get("/interfaces", response_model=list)
def list_network_interfaces(current_user=Depends(get_current_active_admin)):
    interfaces = []
    for name, addrs in psutil.net_if_addrs().items():
        iface = {"interface": name, "ip": "", "mac": "", "type": "", "status": ""}
        for addr in addrs:
            if addr.family.name == 'AF_INET':
                iface["ip"] = addr.address
            elif addr.family.name == 'AF_LINK':
                iface["mac"] = addr.address
        iface["type"] = "ethernet" if "eth" in name or "en" in name else "wifi" if "wi" in name else "unknown"
        iface["status"] = "connected" if name in psutil.net_if_stats() and psutil.net_if_stats()[name].isup else "disconnected"
        interfaces.append(iface)
    return interfaces

@router.post("/set-ip", response_model=dict)
def set_interface_ip(interface: str, ip: str, mask: str, current_user=Depends(get_current_active_admin)):
    try:
        system = platform.system()
        if system == "Windows":
            cmd = f'netsh interface ip set address name="{interface}" static {ip} {mask}'
        elif system == "Linux":
            cmd = f"sudo ifconfig {interface} {ip} netmask {mask} up"
        else:
            raise Exception("Unsupported OS")
        subprocess.run(cmd, shell=True, check=True)
        return {"msg": f"IP set for {interface}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/toggle", response_model=dict)
def toggle_interface(interface: str, enable: bool, current_user=Depends(get_current_active_admin)):
    try:
        system = platform.system()
        if system == "Windows":
            state = "enabled" if enable else "disabled"
            cmd = f'netsh interface set interface "{interface}" admin={state}'
        elif system == "Linux":
            state = "up" if enable else "down"
            cmd = f"sudo ifconfig {interface} {state}"
        else:
            raise Exception("Unsupported OS")
        subprocess.run(cmd, shell=True, check=True)
        return {"msg": f"Interface {interface} {'enabled' if enable else 'disabled'}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
