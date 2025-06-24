# job_discovery/job_filters.py
def filter_jobs(jobs, min_budget=50, keywords=None):
    filtered = []
    for job in jobs:
        if job['budget'] < min_budget:
            continue
        if keywords:
            if not any(k.lower() in job['title'].lower() or k.lower() in job['description'].lower() for k in keywords):
                continue
        filtered.append(job)
    return filtered
