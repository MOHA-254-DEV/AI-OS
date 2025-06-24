# job_matcher/test_resume_optimizer.py
from smart_resume_generator import generate_and_match

resume_text = """
John Doe
Frontend Developer
Experience in React, Vue, HTML/CSS, JavaScript
"""

job_listings = [
    {"title": "React Developer", "description": "Looking for expert in React, Redux, JavaScript, CSS", "url": "https://freelance.com/job/react"},
    {"title": "Full Stack Dev", "description": "Node.js, MongoDB, frontend skills like React or Angular", "url": "https://upwork.com/job/fs"},
    {"title": "Web Designer", "description": "Creative designer with HTML, CSS, UI/UX tools", "url": "https://freelancer.com/job/webui"}
]

result = generate_and_match(resume_text, job_listings)

print("Optimized Resume:\n", result["optimized_resume"])
print("\nTop Job Matches:")
for job in result["best_jobs"]:
    print(f"{job['title']} ({job['match_score']*100:.2f}% match) -> {job['url']}")
