# cover_letter/test.py

from builder import build_cover_letters_for_jobs

applicant = {
    "name": "Jane Doe",
    "experience_area": "Full Stack Web Development",
    "skills": ["React", "Node.js", "GraphQL", "MongoDB"],
    "years_experience": 5,
    "achievements": "led multiple successful product launches, mentored junior developers"
}

jobs = [
    {"title": "React Developer", "hiring_manager": "Mr. Smith"},
    {"title": "Full Stack Engineer", "hiring_manager": "Ms. Johnson"},
]

results = build_cover_letters_for_jobs(applicant, jobs)

for res in results:
    print(f"\n--- Cover Letter for {res['job_title']} ---\n")
    print(res["cover_letter"])
