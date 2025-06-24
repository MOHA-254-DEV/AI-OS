from agents.job_finder import JobFinder
from utils.logger import log_task

finder = JobFinder()

async def remotive_search(args):
    query = args[0] if args else "python"
    result = finder.fetch_remotive_jobs(query)
    log_task("remotive_search", "completed", str(result))
    return result

async def remoteok_search(args):
    query = args[0] if args else "developer"
    result = finder.fetch_remoteok_jobs(query)
    log_task("remoteok_search", "completed", str(result))
    return result

async def freelancer_search(args):
    query = args[0] if args else "design"
    result = finder.fetch_freelancer_jobs(query)
    log_task("freelancer_search", "completed", str(result))
    return result

async def list_jobs(args):
    result = finder.list_saved_jobs()
    return result

def register():
    return {
        "remotive_search": remotive_search,
        "remoteok_search": remoteok_search,
        "freelancer_search": freelancer_search,
        "list_jobs": list_jobs
    }
