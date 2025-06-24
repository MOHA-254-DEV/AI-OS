from string import Template


class ResumeGenerator:
    def __init__(self, name, email, phone, linkedin, summary, skills, experience, education):
        """
        Initializes the ResumeGenerator with personal and professional information.

        :param name: Full name of the candidate.
        :param email: Email address.
        :param phone: Phone number.
        :param linkedin: LinkedIn profile URL.
        :param summary: Professional summary.
        :param skills: Comma-separated list or formatted string of skills.
        :param experience: Multiline experience section.
        :param education: Educational background.
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.linkedin = linkedin
        self.summary = summary
        self.skills = skills
        self.experience = experience
        self.education = education

    def generate_resume(self) -> str:
        """
        Generate a plain-text resume in markdown format.

        :return: A formatted resume string.
        """
        resume_template = Template(
            """# ${name}

**Email:** ${email}  
**Phone:** ${phone}  
**LinkedIn:** [${linkedin}](${linkedin})

---

## 💼 Summary  
${summary}

## 🛠️ Skills  
${skills}

## 📈 Experience  
${experience}

## 🎓 Education  
${education}
"""
        )

        return resume_template.substitute(
            name=self.name,
            email=self.email,
            phone=self.phone,
            linkedin=self.linkedin,
            summary=self.summary,
            skills=self.skills,
            experience=self.experience,
            education=self.education
        )


# 🔧 Example usage
def main():
    name = "Jane Smith"
    email = "janesmith@example.com"
    phone = "+1234567890"
    linkedin = "https://www.linkedin.com/in/janesmith"
    summary = "Experienced software developer with a passion for writing clean, scalable code and leading agile teams."
    skills = "- Python\n- JavaScript\n- React\n- SQL\n- HTML/CSS"
    experience = (
        "- **Senior Developer**, XYZ Corp (2019–2024): Led frontend and backend development for SaaS platforms.\n"
        "- **Junior Developer**, ABC Tech (2017–2019): Supported application development and bug fixes."
    )
    education = "- B.Sc. in Computer Science, University of ABC (2013–2017)"

    generator = ResumeGenerator(name, email, phone, linkedin, summary, skills, experience, education)
    print(generator.generate_resume())


if __name__ == "__main__":
    main()
