from .web_searcher import WebSearcher
from .result_parser import ResultParser
from .search_strategy import SearchStrategy
import logging
import time

class KnowledgeIntegrator:
    def __init__(self, max_results=1):
        self.searcher = WebSearcher()
        self.parser = ResultParser()
        self.strategy = SearchStrategy()
        self.max_results = max_results

        # Structured logger
        self.logger = logging.getLogger("KnowledgeIntegrator")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def augment_task(self, task_context: dict) -> dict:
        """
        Augments the given task context with external web information.
        :param task_context: Dictionary with task data (should contain a clear goal or description).
        :return: Augmented task_context with external_info field.
        """
        try:
            query = self.strategy.build_query(task_context)
            if not query:
                self.logger.warning("Query building failed: No query generated.")
                return task_context

            self.logger.info(f"Searching web for: '{query}'")
            results = self.searcher.search(query)

            if not results:
                self.logger.warning("Web search yielded no results.")
                return task_context

            attempts = 0
            for result in results[:self.max_results]:
                try:
                    url = result.get("link") or result.get("url")
                    if not url:
                        continue

                    self.logger.info(f"Extracting content from: {url}")
                    snippet = self.parser.extract_text(url)

                    if snippet:
                        task_context["external_info"] = {
                            "source": url,
                            "summary": snippet
                        }
                        self.logger.info(f"Task successfully enriched with info from {url}")
                        return task_context
                except Exception as inner_ex:
                    self.logger.warning(f"Failed to extract from result #{attempts + 1}: {inner_ex}")
                attempts += 1

            self.logger.warning("All top results failed to yield usable content.")
            return task_context

        except Exception as e:
            self.logger.error(f"[FATAL] Unexpected error in augment_task: {str(e)}", exc_info=True)
            return task_context

