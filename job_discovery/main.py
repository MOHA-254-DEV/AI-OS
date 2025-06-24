# job_discovery/main.py
from fastapi import FastAPI, Query
from crawler import gather_jobs
from job_filters import filter_jobs
import json

app = FastAPI()
CACHE_FILE = "job_discovery/job_cache.json"

@app.get("/jobs")
def get_jobs(min_budget: int = 50, keywords: str = Query(None)):
    keyword_list = [kw.strip() for kw in keywords.split(",")] if keywords else None
    jobs = gather_jobs(keywords=keyword_list)
    filtered = filter_jobs(jobs, min_budget, keyword_list)

    with open(CACHE_FILE, "w") as f:
        json.dump(filtered, f, indent=2)

    return {"jobs_found": len(filtered), "jobs": filtered}
