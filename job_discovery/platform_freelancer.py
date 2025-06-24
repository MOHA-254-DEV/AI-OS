# job_discovery/platform_freelancer.py
import uuid
from datetime import datetime

def fetch_freelancer_jobs(keywords=None):
    return [
        {
            "id": str(uuid.uuid4()),
            "platform": "Freelancer",
            "title": "SEO Specialist",
            "description": "Optimize our blog for search engines",
            "budget": 80,
            "posted_at": datetime.utcnow().isoformat(),
            "url": "https://www.freelancer.com/job/seo-specialist"
        },
        {
            "id": str(uuid.uuid4()),
            "platform": "Freelancer",
            "title": "Full Stack Developer",
            "description": "Develop an eCommerce web app",
            "budget": 500,
            "posted_at": datetime.utcnow().isoformat(),
            "url": "https://www.freelancer.com/job/fullstack-ecommerce"
        }
    ]
