# marketplace/backend/routers/plugins.py
from fastapi import APIRouter, HTTPException
from models import Plugin

router = APIRouter()

# Mock Plugin Registry
plugins = [
    Plugin(id="plugin_001", name="AutoTranslate", description="Translate docs automatically", version="1.2.0", rating=4.7),
    Plugin(id="plugin_002", name="ImageEditorAI", description="Edit images using AI commands", version="2.1.3", rating=4.5),
    Plugin(id="plugin_003", name="MarketPredictor", description="Analyze and predict trading trends", version="3.0.0", rating=4.8),
]

@router.get("/plugins")
def get_plugins():
    return plugins

@router.post("/plugins/install/{plugin_id}")
def install_plugin(plugin_id: str):
    matching = next((p for p in plugins if p.id == plugin_id), None)
    if not matching:
        raise HTTPException(status_code=404, detail="Plugin not found")
    # Simulate installation logic
    # Save to disk, sandbox, or enable in registry
    return {"status": "installed", "plugin": matching.dict()}
