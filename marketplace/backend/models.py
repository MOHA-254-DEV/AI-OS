# marketplace/backend/models.py
from pydantic import BaseModel

class Plugin(BaseModel):
    id: str
    name: str
    description: str
    version: str
    rating: float
