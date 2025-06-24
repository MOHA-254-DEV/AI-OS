# job_matcher/smart_resume_generator.py
from resume_optimizer import optimize_resume
from job_matcher_engine import match_jobs_to_resume

def generate_and_match(resume_text, job_listings):
    best_matches = match_jobs_to_resume(resume_text, job_listings)

    optimized = optimize_resume(resume_text, best_matches[0]["description"])

    return {
        "optimized_resume": optimized["optimized_resume"],
        "best_jobs": best_matches[:5]
    }
