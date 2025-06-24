# job_discovery/platform_upwork.py
import uuid
from datetime import datetime

def fetch_upwork_jobs(keywords=None):
    return [
        {
            "id": str(uuid.uuid4()),
            "platform": "Upwork",
            "title": "Graphic Designer Needed for Logo",
            "description": "Design a modern logo for a tech startup",
            "budget": 100,
            "posted_at": datetime.utcnow().isoformat(),
            "url": "https://www.upwork.com/job/graphic-logo"
        },
        {
            "id": str(uuid.uuid4()),
            "platform": "Upwork",
            "title": "React Developer",
            "description": "Build a dashboard using React",
            "budget": 250,
            "posted_at": datetime.utcnow().isoformat(),
            "url": "https://www.upwork.com/job/react-dashboard"
        }
    ]
