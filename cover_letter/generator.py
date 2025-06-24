# cover_letter/generator.py

from templates import DEFAULT_TEMPLATE

def generate_cover_letter(applicant, job, custom_motivation):
    filled = DEFAULT_TEMPLATE.format(
        hiring_manager=job.get("hiring_manager", "Hiring Manager"),
        job_title=job["title"],
        experience_area=applicant["experience_area"],
        skills=", ".join(applicant["skills"]),
        years_experience=applicant["years_experience"],
        achievements=applicant["achievements"],
        custom_motivation=custom_motivation,
        applicant_name=applicant["name"]
    )
    return filled
