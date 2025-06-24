# auto_application/main.py

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from application_engine import auto_apply
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Auto Application API",
    description="Automatically apply to jobs with generated resumes and cover letters.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Models --------------------

class Job(BaseModel):
    title: str = Field(..., example="Python Developer")
    platform: str = Field(..., example="Upwork")
    url: str = Field(..., example="https://www.upwork.com/job/xyz")

class Applicant(BaseModel):
    name: str = Field(..., example="Jane Doe")
    email: Optional[EmailStr] = Field(None, example="jane@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")
    linkedin: Optional[str] = Field(None, example="https://linkedin.com/in/janedoe")
    skills: List[str] = Field(..., example=["Python", "FastAPI", "SQL"])
    summary: Optional[str] = Field(None, example="Experienced backend developer with 5+ years in API design.")
    experience: Optional[str] = Field(None, example="Backend Developer at XYZ Corp (2020-2024)")
    education: Optional[str] = Field(None, example="BSc in Computer Science, MIT")
    custom_paragraph: Optional[str] = Field(
        default="I have worked on similar projects and consistently exceed expectations.",
        example="I built a similar project with Django and PostgreSQL that scaled to 1M users."
    )

# -------------------- Routes --------------------

@app.post("/apply", summary="Apply to a job automatically", tags=["Application"])
def apply_to_job(
    job: Job = Body(..., description="Job information"),
    applicant_data: Applicant = Body(..., description="Applicant profile")
):
    """
    Automatically generates a resume and cover letter, then simulates a job application.
    """
    logger.info(f"[AUTO APPLY API] Received application request for job: {job.title}")
    try:
        result = auto_apply(job.dict(), applicant_data.dict())
        if result.get("status") != "submitted":
            logger.warning(f"[AUTO APPLY API] Application failed: {result}")
            raise HTTPException(status_code=400, detail=result.get("message", "Failed to apply."))
        logger.info(f"[AUTO APPLY API] Successfully applied to {job.title} on {job.platform}")
        return result
    except Exception as e:
        logger.exception(f"Unhandled error during application submission: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Application failed: {str(e)}")

# -------------------- Health Check --------------------

@app.get("/", tags=["Health"])
def root():
    return {"status": "Auto Application API is running"}
