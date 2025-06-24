import pdfkit
import os

def export_to_pdf(html_path="reporting/output/report.html", pdf_path="reporting/output/report.pdf"):
    if not os.path.exists(html_path):
        raise FileNotFoundError("HTML report does not exist.")
    pdfkit.from_file(html_path, pdf_path)
    print(f"[PDF] Exported report to {pdf_path}")

if __name__ == "__main__":
    export_to_pdf()
