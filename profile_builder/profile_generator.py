# profile_builder/profile_generator.py

from jinja2 import Template

def generate_profile_html(data, template_str):
    template = Template(template_str)
    return template.render(**data)
