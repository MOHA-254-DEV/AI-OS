from jinja2 import Template
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AIOS Report</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f4f4f4; }
        .section { margin-bottom: 30px; }
        h2 { background: #333; color: #fff; padding: 10px; }
        pre { background: #eee; padding: 10px; border-radius: 6px; }
    </style>
</head>
<body>
    <h1>AIOS System Report</h1>
    <p>Generated: {{ generated_at }}</p>
    {% for section, content in sections.items() %}
    <div class="section">
        <h2>{{ section }}</h2>
        <pre>{{ content | tojson(indent=2) }}</pre>
    </div>
    {% endfor %}
</body>
</html>
"""

def generate_html(data, output_path="reporting/output/report.html"):
    tmpl = Template(HTML_TEMPLATE)
    html = tmpl.render(**data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html)
    print(f"[HTML] Report saved at {output_path}")

if __name__ == "__main__":
    from report_engine import ReportEngine
    engine = ReportEngine()
    engine.add_data_source("test", lambda: {"status": "ok", "value": 42})
    report_data = engine.collect_data()
    generate_html(report_data)
