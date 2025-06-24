# voice_interface/launch.py
from voice_application_controller import start_voice_loop

applicant_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+123456789",
    "linkedin": "linkedin.com/in/johndoe",
    "summary": "Experienced web developer",
    "skills": ["React", "Node.js", "MongoDB"],
    "experience": "5 years in full-stack development",
    "education": "B.Sc. in Computer Science",
    "custom_paragraph": "I specialize in building scalable frontend architectures."
}

start_voice_loop(applicant_data)
