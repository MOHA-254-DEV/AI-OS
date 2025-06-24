import requests
from bs4 import BeautifulSoup
import re
import random
from utils.logger import logger


class MarketingAgent:
    def __init__(self):
        self.cta_templates = [
            "🚀 Boost your {niche} with {product} today!",
            "🔥 Discover how {product} can grow your {niche}!",
            "⚡ Unlock {benefit} using {product}. Try it now!",
            "🎯 Ready to take your {niche} to the next level with {product}?",
            "💡 Experience {benefit} like never before with {product}!"
        ]

    def generate_ad_copy(self, niche: str, product: str, benefit: str = "better results"):
        """
        Generate persuasive ad copy based on a random call-to-action template.
        """
        logger.info(f"[AD_COPY] Generating for product='{product}', niche='{niche}'")
        try:
            template = random.choice(self.cta_templates)
            ad_copy = template.format(niche=niche, product=product, benefit=benefit)
            logger.info(f"[AD_COPY] Output: {ad_copy}")
            return ad_copy
        except Exception as e:
            logger.error(f"[AD_COPY] Failed: {e}")
            return "Try our amazing solution today!"

    def seo_optimize_title(self, topic: str):
        """
        Generates an SEO-optimized title using keywords and search-friendly phrasing.
        """
        logger.info(f"[SEO_TITLE] Topic received: {topic}")
        try:
            base = topic.lower().strip()
            words = [w.capitalize() for w in re.findall(r'\b\w{3,}\b', base)]
            if not words:
                return "Ultimate Guide to Growth"
            focus = ", ".join(words[:3])
            title = f"Top {random.randint(5, 12)} Strategies for {focus} Success in {datetime.now().year}"
            logger.info(f"[SEO_TITLE] Output: {title}")
            return title
        except Exception as e:
            logger.error(f"[SEO_TITLE] Failed: {e}")
            return "Learn Top Strategies for Online Success"

    def crawl_keywords(self, url: str):
        """
        Extracts top 10 most frequent non-trivial words from the web page content.
        """
        logger.info(f"[KEYWORD_CRAWLER] URL: {url}")
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            text = soup.get_text(separator=' ', strip=True).lower()
            words = re.findall(r'\b[a-z]{4,}\b', text)
            freq = {}
            for word in words:
                freq[word] = freq.get(word, 0) + 1
            sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
            keywords = [word for word, _ in sorted_freq[:10]]
            logger.info(f"[KEYWORD_CRAWLER] Top keywords: {keywords}")
            return keywords
        except requests.RequestException as e:
            logger.error(f"[KEYWORD_CRAWLER] Request error: {e}")
        except Exception as e:
            logger.error(f"[KEYWORD_CRAWLER] Parsing error: {e}")
        return []

    def summarize_page(self, url: str, max_sentences=3):
        """
        Summarizes a webpage by extracting and selecting key content sentences.
        """
        logger.info(f"[SUMMARY] Starting summarization for {url}")
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            full_text = soup.get_text(separator=' ', strip=True)
            sentences = re.split(r'(?<=[.!?])\s+', full_text)
            valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 50][:max_sentences]
            summary = " ".join(valid_sentences)
            logger.info(f"[SUMMARY] Summary generated: {summary}")
            return summary if summary else "Content summary not available."
        except requests.RequestException as e:
            logger.error(f"[SUMMARY] Network error: {e}")
        except Exception as e:
            logger.error(f"[SUMMARY] Unexpected failure: {e}")
        return "Summary not available."

