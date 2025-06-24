# job_discovery/crawler.py
from platform_upwork import fetch_upwork_jobs
from platform_freelancer import fetch_freelancer_jobs

def gather_jobs(keywords=None):
    jobs = []
    jobs += fetch_upwork_jobs(keywords)
    jobs += fetch_freelancer_jobs(keywords)
    return jobs
