import random
import logging

class PluginPersonalityAdapter:
    def __init__(self, plugin_module, agent_profile, enable_logging=False):
        """
        Initialize the PluginPersonalityAdapter.

        :param plugin_module: The plugin module to be executed.
        :param agent_profile: The agent's profile that contains communication preferences.
        :param enable_logging: Whether to enable debug logging.
        """
        self.plugin = plugin_module
        self.profile = agent_profile
        self.logger = logging.getLogger("PluginAdapter")
        if enable_logging and not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)

    def execute(self, *args, **kwargs):
        """
        Execute the plugin's `run` method and adapt the result based on the agent's profile.
        """
        verbosity = self.profile.get("verbosity", 0.5)
        style = self.profile.get("communication_style", "balanced")

        if not hasattr(self.plugin, "run"):
            return self.handle_error("Plugin lacks a 'run()' method.")

        try:
            raw_result = self.plugin.run(*args, **kwargs)
            self.logger.debug(f"Raw result: {raw_result}")
            adapted_result = self._apply_verbosity(raw_result, verbosity, style)

            return {
                "result": adapted_result,
                "meta": {
                    "style": style,
                    "verbosity": verbosity,
                    "status": "success"
                }
            }

        except Exception as e:
            return self.handle_error(f"Plugin execution failed: {str(e)}")

    def _apply_verbosity(self, result, verbosity, style):
        """
        Adjusts verbosity and communication style of the result.
        """
        if isinstance(result, str):
            return self._stylize_text(result, verbosity, style)

        elif isinstance(result, list):
            if verbosity < 0.3:
                return result[:2]
            elif verbosity > 0.7:
                return result + ["[End of detailed list]"]
            else:
                return result[:3]

        elif isinstance(result, dict):
            if verbosity < 0.3:
                return {k: result[k] for k in ('summary', 'key_info') if k in result}
            elif verbosity > 0.7:
                return {**result, "extra_info": "All available data shown."}
            else:
                return result

        return self.handle_unknown_type(result)

    def _stylize_text(self, text, verbosity, style):
        """
        Enhances string output based on communication style and verbosity.
        """
        message = text.strip()

        if verbosity > 0.7:
            message += " Please explore the details thoroughly."

        if style == "empathetic":
            return f"😊 Just so you know: {message}"
        elif style == "formal":
            return f"Kindly note: {message}"
        elif style == "concise":
            return message.split('.')[0] + '.'
        elif style == "expressive":
            return f"🔥 Here's what I found: {message}"
        else:
            return message

    def handle_error(self, msg):
        """ Consistent error response. """
        self.logger.error(msg)
        return {
            "error": msg,
            "meta": {
                "status": "error"
            }
        }

    def handle_unknown_type(self, result):
        """ Handles unformatted types. """
        self.logger.warning("Unknown result type. Returning raw.")
        return result
