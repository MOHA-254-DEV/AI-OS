# cover_letter/builder.py

from generator import generate_cover_letter

def build_cover_letters_for_jobs(applicant_profile, jobs):
    letters = []
    for job in jobs:
        motivation = f"I admire your work in {job['title']} and I’m excited about contributing to it."
        letter = generate_cover_letter(applicant_profile, job, motivation)
        letters.append({
            "job_title": job["title"],
            "cover_letter": letter
        })
    return letters
