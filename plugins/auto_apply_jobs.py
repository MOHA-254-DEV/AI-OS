from agents.job_finder import JobFinder
from utils.logger import logger
import asyncio

async def apply_jobs(args):
    keyword = args[0] if args else "virtual assistant"
    finder = JobFinder()
    jobs = await finder.find_remote_jobs(keyword)
    for job in jobs:
        logger.info(f"Found Job: {job['title']} → {job['link']}")

def register():
    return {
        "apply_jobs": apply_jobs
    }
