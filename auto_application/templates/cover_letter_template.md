from string import Template


class CoverLetterGenerator:
    def __init__(self, client_name, job_title, platform, skills, custom_paragraph, applicant_name):
        """
        Initializes the CoverLetterGenerator with user input.
        :param client_name: Name of the client or company.
        :param job_title: Job title or role being applied for.
        :param platform: Platform where the job was posted (e.g., Upwork, Freelancer).
        :param skills: Skills relevant to the job.
        :param custom_paragraph: A paragraph tailored to the job post.
        :param applicant_name: Your (applicant's) name.
        """
        self.client_name = client_name
        self.job_title = job_title
        self.platform = platform
        self.skills = skills
        self.custom_paragraph = custom_paragraph
        self.applicant_name = applicant_name

    def generate_cover_letter(self) -> str:
        """
        Generates a personalized cover letter using string templating.
        :return: A formatted cover letter string.
        """
        letter_template = Template(
            """Subject: Application for ${job_title} Position

Dear ${client_name},

I am writing to express my interest in the ${job_title} position posted on ${platform}. With strong experience in ${skills}, I am confident in my ability to contribute significantly to your project.

${custom_paragraph}

I am excited about the opportunity to collaborate and deliver results that align with your goals. Thank you for considering my application—I look forward to the opportunity to discuss further how I can help you succeed.

Sincerely,  
${applicant_name}
"""
        )

        # Populate template
        return letter_template.substitute(
            client_name=self.client_name,
            job_title=self.job_title,
            platform=self.platform,
            skills=self.skills,
            custom_paragraph=self.custom_paragraph,
            applicant_name=self.applicant_name
        )


# 🔧 Example usage
def main():
    # Replace these with user-supplied values (from form, CLI, etc.)
    client_name = "John Doe"
    job_title = "Web Developer"
    platform = "Upwork"
    skills = "HTML, CSS, JavaScript, and React"
    custom_paragraph = (
        "I have successfully completed several projects involving responsive web design and interactive interfaces. "
        "My attention to detail and commitment to high-quality code ensure client satisfaction."
    )
    applicant_name = "Jane Smith"

    # Generate and print letter
    generator = CoverLetterGenerator(client_name, job_title, platform, skills, custom_paragraph, applicant_name)
    letter = generator.generate_cover_letter()
    print(letter)


if __name__ == "__main__":
    main()
