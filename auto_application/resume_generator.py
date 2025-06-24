# auto_application/resume_generator.py

import os
from jinja2 import Template, TemplateError
import pdfkit
import logging
import uuid

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_resume(data: dict, output_dir: str = "generated") -> str:
    """
    Generates a resume in PDF format using a markdown Jinja2 template.

    Args:
        data (dict): Dictionary containing resume fields.
        output_dir (str): Directory to store the generated files.

    Returns:
        str: Path to the generated PDF file.
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Paths
        template_path = os.path.join(os.path.dirname(__file__), "templates", "resume_template.md")
        if not os.path.isfile(template_path):
            raise FileNotFoundError(f"Resume template not found at: {template_path}")

        # Generate unique filenames
        filename_prefix = f"resume_{uuid.uuid4().hex[:8]}"
        markdown_path = os.path.join(output_dir, f"{filename_prefix}.md")
        pdf_path = os.path.join(output_dir, f"{filename_prefix}.pdf")

        # Load and render template
        with open(template_path, "r", encoding="utf-8") as f:
            template = Template(f.read())

        rendered_content = template.render(data)

        # Save markdown
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(rendered_content)
        logger.info(f"[📝] Resume markdown written to {markdown_path}")

        # Convert markdown to PDF
        try:
            pdfkit.from_file(markdown_path, pdf_path)
            logger.info(f"[✅] Resume PDF generated at {pdf_path}")
        except Exception as pdf_error:
            logger.warning(f"[⚠️] PDFKit failed: {pdf_error}")
            raise RuntimeError("PDF generation failed. Ensure `wkhtmltopdf` is installed.")

        return pdf_path

    except TemplateError as te:
        logger.error(f"[❌] Template error: {te}")
        raise

    except Exception as e:
        logger.error(f"[❌] Resume generation failed: {e}")
        raise
