from jinja2 import Template
import pdfkit
import os
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_cover_letter(job: dict, applicant_data: dict, output_dir="generated") -> str | None:
    """
    Generates a cover letter PDF for a job application using a Jinja2 Markdown template.
    
    :param job: Dictionary with job details (must include 'title', 'platform')
    :param applicant_data: Dictionary with applicant info (must include 'name', 'skills', optional 'custom_paragraph')
    :param output_dir: Directory to store the generated files
    :return: Path to the generated PDF cover letter or None if error
    """
    try:
        # Validate required fields
        for field in ['title', 'platform']:
            if field not in job:
                raise ValueError(f"Missing job field: {field}")
        for field in ['name', 'skills']:
            if field not in applicant_data:
                raise ValueError(f"Missing applicant field: {field}")

        template_path = os.path.join("auto_application", "templates", "cover_letter_template.md")
        if not os.path.isfile(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        os.makedirs(output_dir, exist_ok=True)
        filename_prefix = f"{job['title'].replace(' ', '_').lower()}_{uuid.uuid4().hex[:8]}"
        md_file_path = os.path.join(output_dir, f"{filename_prefix}_cover_letter.md")
        pdf_file_path = os.path.join(output_dir, f"{filename_prefix}_cover_letter.pdf")

        # Read and render template
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
        template = Template(template_content)

        rendered_md = template.render({
            "client_name": job.get("client_name", "Hiring Manager"),
            "job_title": job["title"],
            "platform": job["platform"],
            "skills": ", ".join(applicant_data["skills"]),
            "custom_paragraph": applicant_data.get("custom_paragraph", "I have worked on similar projects and consistently exceeded expectations."),
            "name": applicant_data["name"]
        })

        # Write Markdown file
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(rendered_md)
        logger.info(f"Markdown cover letter saved to: {md_file_path}")

        # Convert to PDF
        try:
            pdfkit.from_file(md_file_path, pdf_file_path)
            logger.info(f"PDF cover letter generated at: {pdf_file_path}")
        except Exception as pdf_err:
            logger.warning(f"PDFKit conversion failed: {pdf_err}")
            raise RuntimeError("PDF generation failed. Ensure wkhtmltopdf is installed.")

        return pdf_file_path

    except Exception as e:
        logger.error(f"Failed to generate cover letter: {str(e)}")
        return None
