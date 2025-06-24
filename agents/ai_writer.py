# ai_writer.py

import os
import openai
import logging

class AIWriter:
    def __init__(self, model="gpt-4", temperature=0.7, use_mock=False, api_key=None):
        """
        Initializes the AIWriter.

        :param model: OpenAI model to use (e.g., "gpt-4", "gpt-3.5-turbo").
        :param temperature: Controls randomness in generation.
        :param use_mock: If True, mock results are returned instead of calling the API.
        :param api_key: Optional OpenAI API key. Defaults to environment variable.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.use_mock = use_mock
        self.model = model
        self.temperature = temperature

        if not self.api_key and not use_mock:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY environment variable or pass `api_key`.")

        if not self.use_mock:
            openai.api_key = self.api_key

        # Setup logger
        self.logger = logging.getLogger("AIWriter")
        self._configure_logger()

    def _configure_logger(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def rewrite_product(self, title: str, tone: str = "exciting", max_tokens: int = 100) -> str:
        """
        Rewrite a product title with a specific tone.

        :param title: The original product title.
        :param tone: The desired tone (e.g., "professional", "funny", "luxurious").
        :param max_tokens: Max token limit for the completion.
        :return: A rewritten product title or a mock/error response.
        """
        if not title:
            return "[Error] Title is required."

        if self.use_mock:
            return f"[Mocked] Introducing the amazing {title}! A must-have for your collection."

        prompt = (
            f"Rewrite the following product title in a persuasive, {tone} tone:\n"
            f"Original: {title}\n"
            f"New:"
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative and persuasive product copywriter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
            )

            result = response.choices[0].message['content'].strip()
            self.logger.info(f"[AIWriter] Rewritten title: {result}")
            return result

        except openai.error.OpenAIError as e:
            self.logger.error(f"[AIWriter] OpenAI API error: {e}")
            return f"[Error] API error: {str(e)}"

        except Exception as e:
            self.logger.exception("[AIWriter] Unexpected exception:")
            return f"[Error] Unexpected failure: {str(e)}"

