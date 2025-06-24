# profile_builder/test_profile.py

from profile_generator import generate_profile_html
from exporter import save_as_html, export_to_pdf, export_to_json

profile_data = {
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "123-456-7890",
    "summary": "Senior Full Stack Developer with over 10 years of experience in scalable web applications.",
    "skills": ["Python", "React", "Node.js", "AWS", "Docker"],
    "experience": [
        {
            "title": "Lead Developer",
            "company": "TechCorp",
            "duration": "2018–2023",
            "description": "Led a team of developers to deliver enterprise apps."
        },
        {
            "title": "Software Engineer",
            "company": "DevSoft",
            "duration": "2014–2018",
            "description": "Built core modules for e-commerce platforms."
        }
    ],
    "education": "B.Sc. in Computer Science, MIT"
}

template_path = Path("profile_builder/profile_template.html").read_text()
html_content = generate_profile_html(profile_data, template_path)

save_as_html(html_content, "profile_builder/output/profile.html")
export_to_pdf("profile_builder/output/profile.html", "profile_builder/output/profile.pdf")
export_to_json(profile_data, "profile_builder/output/profile.json")
