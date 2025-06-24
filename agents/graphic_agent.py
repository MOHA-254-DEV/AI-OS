import os
import requests
from utils.logger import logger
from secure.crypto_util import decrypt_data


class GraphicAgent:
    def __init__(self, token_path="secure/secrets/image_api.token"):
        """
        Initializes the GraphicAgent and securely loads the API key.
        """
        self.api_key = None
        self.api_url = "https://api.stablediffusionapi.com/v3/text2img"

        if os.path.exists(token_path):
            try:
                with open(token_path, "rb") as f:
                    self.api_key = decrypt_data(f.read()).strip()
                logger.info("GraphicAgent API key loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to decrypt image API token: {e}")
        else:
            logger.warning(f"API token file not found at {token_path}.")

    def generate_image(self, prompt: str, output: str = "output.png", width=512, height=512, steps=30) -> str:
        """
        Generates an image using Stable Diffusion API from a text prompt.

        :param prompt: The text prompt to visualize.
        :param output: Path to save the resulting image.
        :param width: Image width in pixels.
        :param height: Image height in pixels.
        :param steps: Number of diffusion steps.
        :return: Path to saved image or None if failed.
        """
        if not self.api_key:
            logger.error("Missing API key. Image generation aborted.")
            return None

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            logger.info(f"Sending request to Stable Diffusion API with prompt: {prompt}")
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            image_url = result.get("output", [None])[0]

            if not image_url:
                logger.error("Stable Diffusion API returned no image URL.")
                return None

            logger.info(f"Image URL received: {image_url}")
            img_data = requests.get(image_url).content

            with open(output, "wb") as f:
                f.write(img_data)

            logger.info(f"Image successfully saved to {output}")
            return output

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error during image generation: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during image generation: {e}")

        return None
