import logging

class SearchStrategy:
    def __init__(self):
        self.logger = logging.getLogger("SearchStrategy")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.query_templates = {
            "marketing": lambda desc: f"latest marketing trends in {desc}",
            "pricing": lambda desc: f"current market price for {desc}",
            "legal": lambda desc: f"recent legal changes in {desc}",
            "code": lambda desc: f"python best practices for {desc}",
        }

    def build_query(self, task_context: dict) -> str:
        """
        Build a search query based on the task type and description.

        :param task_context: A dict with keys like 'type' and 'description'.
        :return: Search query string.
        """
        task_type = task_context.get("type", "general").strip().lower()
        description = task_context.get("description", "").strip()

        if not description:
            self.logger.warning("Task description is missing. Defaulting to 'general information'.")
            description = "general information"

        query = self._build_query_by_type(task_type, description)
        self.logger.info(f"Constructed query [{task_type}]: {query}")
        return query

    def _build_query_by_type(self, task_type: str, description: str) -> str:
        """
        Generate query using the mapped strategy or fallback.

        :param task_type: Type of task (e.g., marketing, code, etc.)
        :param description: Main task content.
        :return: String search query.
        """
        if task_type in self.query_templates:
            return self.query_templates[task_type](description)
        else:
            self.logger.debug(f"No specific query format for task type '{task_type}'. Using description only.")
            return description
