# dev_agent.py

import shutil
import os
from typing import List, Dict, Union
from utils.logger import logger

class DevAgent:
    def __init__(self, scaffold_root: str = "scaffolds", output_dir: str = "generated_projects"):
        """
        Initializes the DevAgent with directories for scaffolds and generated projects.
        """
        self.scaffold_root = os.path.abspath(scaffold_root)
        self.output_dir = os.path.abspath(output_dir)

        try:
            os.makedirs(self.scaffold_root, exist_ok=True)
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"[Init] Scaffold root: {self.scaffold_root}")
            logger.info(f"[Init] Output directory: {self.output_dir}")
        except Exception as e:
            logger.exception(f"[Init] Failed to initialize directories: {e}")
            raise

    def list_templates(self) -> List[str]:
        """
        Lists all available scaffold templates.

        :return: A list of template names.
        """
        try:
            templates = [
                entry.name for entry in os.scandir(self.scaffold_root)
                if entry.is_dir()
            ]
            logger.info(f"[ListTemplates] Found {len(templates)} templates.")
            return templates
        except Exception as e:
            logger.error(f"[ListTemplates] Failed to list templates: {e}")
            return []

    def generate_project(self, template: str, project_name: str) -> Dict[str, Union[str, Dict]]:
        """
        Generates a new project from a given template.

        :param template: The name of the scaffold template.
        :param project_name: The desired name for the new project.
        :return: A dictionary with status and project info.
        """
        src_path = os.path.join(self.scaffold_root, template)
        dest_path = os.path.join(self.output_dir, project_name)

        if not os.path.isdir(src_path):
            logger.error(f"[Generate] Template '{template}' does not exist at: {src_path}")
            return {
                "status": "error",
                "message": f"Template '{template}' not found.",
                "template_path": src_path
            }

        if os.path.exists(dest_path):
            logger.warning(f"[Generate] Project '{project_name}' already exists at: {dest_path}")
            return {
                "status": "error",
                "message": f"Project '{project_name}' already exists.",
                "existing_path": dest_path
            }

        try:
            shutil.copytree(src_path, dest_path)
            logger.info(f"[Generate] Successfully scaffolded '{project_name}' from template '{template}'.")

            return {
                "status": "success",
                "project": project_name,
                "template": template,
                "path": os.path.abspath(dest_path)
            }

        except Exception as e:
            logger.exception("[Generate] Error occurred while copying template.")
            return {
                "status": "error",
                "message": "Failed to scaffold project.",
                "details": str(e)
            }
