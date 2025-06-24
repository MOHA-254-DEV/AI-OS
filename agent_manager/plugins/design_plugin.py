# agent_manager/plugins/design_plugin.py

from .plugin_base import PluginBase
import logging
from typing import Dict, Any


class DesignPlugin(PluginBase):
    """
    DesignPlugin handles design-related task types like logo generation,
    UI mockups, and banners.
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("DesignPlugin")
        self.logger.setLevel(logging.INFO)

    def run(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch the design task based on task_data.

        :param task_data: Dictionary with keys 'type' and optional 'payload'
        :return: Dictionary with status and result or error message
        """
        try:
            self.logger.info(f"[DesignPlugin] Task received: {task_data}")

            if not isinstance(task_data, dict) or "type" not in task_data:
                raise ValueError("Invalid task_data: Must be a dict with 'type' field.")

            task_type = task_data["type"]
            payload = task_data.get("payload", {})

            if task_type == "logo":
                result = self._generate_logo(payload)
            elif task_type == "ui_mockup":
                result = self._generate_ui_mockup(payload)
            elif task_type == "banner":
                result = self._generate_banner(payload)
            else:
                raise NotImplementedError(f"Unknown design task type: {task_type}")

            self.logger.info(f"[DesignPlugin] Successfully handled {task_type}")
            return {
                "plugin": "DesignPlugin",
                "status": "success",
                "result": result
            }

        except Exception as e:
            self.logger.error(f"[DesignPlugin] Error: {e}", exc_info=True)
            return {
                "plugin": "DesignPlugin",
                "status": "error",
                "message": str(e)
            }

    def _generate_logo(self, payload: Dict[str, Any]) -> str:
        brand = payload.get("brand", "Unnamed")
        return f"🧠 Logo generated for brand: {brand}"

    def _generate_ui_mockup(self, payload: Dict[str, Any]) -> str:
        pages = payload.get("pages", 1)
        return f"📱 UI mockup created for {pages} page(s)"

    def _generate_banner(self, payload: Dict[str, Any]) -> str:
        size = payload.get("size", "1024x768")
        return f"🎨 Banner designed with size {size}"
