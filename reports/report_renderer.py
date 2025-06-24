import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF
import os

class ReportRenderer:
    def __init__(self, output_dir="output_reports"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def render_chart(self, df: pd.DataFrame, chart_name: str):
        fig = px.bar(df.head(10))
        chart_path = os.path.join(self.output_dir, f"{chart_name}.html")
        fig.write_html(chart_path)
        print(f"[CHART] Saved chart: {chart_path}")
        return chart_path

    def render_html(self, df: pd.DataFrame, summary: str, name="report"):
        html_path = os.path.join(self.output_dir, f"{name}.html")
        df_html = df.to_html(classes='data')
        with open(html_path, "w") as f:
            f.write(f"<h1>AI Report</h1><p>{summary}</p>{df_html}")
        print(f"[HTML] Report saved to {html_path}")
        return html_path

    def render_pdf(self, df: pd.DataFrame, summary: str, name="report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"AI Report Summary:\n{summary}\n\n")

        for col in df.columns:
            pdf.cell(40, 10, f"{col}", ln=True)

        pdf_path = os.path.join(self.output_dir, f"{name}.pdf")
        pdf.output(pdf_path)
        print(f"[PDF] Report saved to {pdf_path}")
        return pdf_path

if __name__ == "__main__":
    df = pd.read_csv("sample_data.csv")
    renderer = ReportRenderer()
    renderer.render_chart(df, "sample_chart")
    renderer.render_html(df, "This is a test summary")
    renderer.render_pdf(df, "This is a test summary")
