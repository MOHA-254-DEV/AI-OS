# auto_application/application_engine.py

import os
import logging
from resume_generator import generate_resume
from cover_letter_generator import generate_cover_letter

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def auto_apply(job: dict, applicant_data: dict) -> dict:
    """
    Automatically applies to a job using the provided applicant data.
    
    :param job: Dictionary containing job details (title, platform, url, etc.)
    :param applicant_data: Dictionary containing applicant profile (name, skills, experience, etc.)
    :return: Result dict indicating status and generated file paths or error
    """
    required_job_fields = ['title', 'platform', 'url']
    missing_fields = [field for field in required_job_fields if field not in job]
    if missing_fields:
        logger.error(f"Missing required job fields: {missing_fields}")
        return {
            "status": "error",
            "message": f"Missing required job field(s): {', '.join(missing_fields)}"
        }

    logger.info(f"[AUTO APPLY] Preparing application for: {job['title']} on {job['platform']}")

    try:
        # Generate resume
        resume_path = generate_resume(applicant_data)
        if not resume_path or not os.path.isfile(resume_path):
            raise FileNotFoundError("Resume file not generated or missing.")

        # Generate cover letter
        cover_letter_path = generate_cover_letter(job, applicant_data)
        if not cover_letter_path or not os.path.isfile(cover_letter_path):
            raise FileNotFoundError("Cover letter file not generated or missing.")

        # Simulate application submission
        logger.info(f"[AUTO APPLY] Resume: {resume_path}")
        logger.info(f"[AUTO APPLY] Cover Letter: {cover_letter_path}")
        logger.info(f"[AUTO APPLY] Submitting application to: {job['url']}")

        return {
            "status": "submitted",
            "job_title": job["title"],
            "platform": job["platform"],
            "resume": resume_path,
            "cover_letter": cover_letter_path
        }

    except Exception as e:
        logger.error(f"[AUTO APPLY] Failed to apply for {job['title']}: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "job_title": job.get("title"),
            "platform": job.get("platform")
        }
