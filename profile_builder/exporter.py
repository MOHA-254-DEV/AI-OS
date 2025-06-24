# profile_builder/exporter.py

import pdfkit
import json
from pathlib import Path

def save_as_html(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

def export_to_pdf(html_file, pdf_file):
    config = pdfkit.configuration()  # Add wkhtmltopdf path if needed
    pdfkit.from_file(html_file, pdf_file, configuration=config)

def export_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
