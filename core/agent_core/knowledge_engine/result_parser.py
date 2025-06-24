import requests
from bs4 import BeautifulSoup
import logging

class ResultParser:
    def __init__(self):
        self.logger = logging.getLogger("ResultParser")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def extract_text(self, url: str, max_paragraphs: int = 5) -> str:
        """
        Extracts readable paragraph text from a given URL.
        
        :param url: Web page URL to fetch and parse.
        :param max_paragraphs: Number of paragraphs to extract.
        :return: Extracted text or a default message.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.124 Safari/537.36"
            }

            self.logger.debug(f"Fetching: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all('p')

            if not paragraphs:
                self.logger.warning(f"No <p> tags found in {url}")
                return "No readable content found."

            extracted_text = " ".join(p.get_text(strip=True) for p in paragraphs[:max_paragraphs])
            self.logger.info(f"Extracted {len(paragraphs[:max_paragraphs])} paragraphs from {url}")
            return extracted_text

        except requests.exceptions.Timeout:
            self.logger.error(f"[TIMEOUT] Failed to fetch {url}")
            return "Error: The request timed out."

        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"[REQUEST ERROR] {url}: {req_err}")
            return "Error: Failed to fetch the web page."

        except Exception as e:
            self.logger.exception(f"[UNEXPECTED ERROR] {url}: {e}")
            return "Error: Could not extract text due to an unexpected issue."
