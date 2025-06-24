import requests
from bs4 import BeautifulSoup
import json
import os

CACHE_PATH = "data/jobs/job_cache.json"

class JobAggregator:
    def __init__(self):
        self.jobs = []
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)

    def scrape_upwork(self):
        print("[SCRAPE] Gathering Upwork jobs...")
        # Simulated jobs due to auth wall
        sample_jobs = [
            {"title": "Logo Design", "platform": "Upwork", "description": "Need a logo for tech startup", "link": "https://upwork.com/job/123"},
            {"title": "Data Entry", "platform": "Upwork", "description": "Copy-paste data project", "link": "https://upwork.com/job/456"}
        ]
        self.jobs.extend(sample_jobs)

    def scrape_fiverr(self):
        print("[SCRAPE] Gathering Fiverr gigs...")
        # Simulated gigs due to dynamic JS
        gigs = [
            {"title": "I will build your website", "platform": "Fiverr", "description": "Full-stack website creation", "link": "https://fiverr.com/gig/321"},
            {"title": "I will create your financial model", "platform": "Fiverr", "description": "Build Excel models", "link": "https://fiverr.com/gig/654"}
        ]
        self.jobs.extend(gigs)

    def scrape_freelancer(self):
        print("[SCRAPE] Gathering Freelancer jobs...")
        url = "https://www.freelancer.com/jobs"
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select(".JobSearchCard-item")
            for item in items[:5]:  # only top 5 for speed
                title = item.select_one(".JobSearchCard-primary-heading-link").text.strip()
                desc = item.select_one(".JobSearchCard-primary-description").text.strip()
                link = "https://www.freelancer.com" + item.select_one(".JobSearchCard-primary-heading-link")['href']
                self.jobs.append({"title": title, "platform": "Freelancer", "description": desc, "link": link})
        except Exception as e:
            print(f"[ERROR] Freelancer scraping failed: {e}")

    def run_all(self):
        self.jobs = []
        self.scrape_upwork()
        self.scrape_fiverr()
        self.scrape_freelancer()
        with open(CACHE_PATH, "w") as f:
            json.dump(self.jobs, f, indent=4)
        print(f"[INFO] Aggregated {len(self.jobs)} jobs.")
        return self.jobs

if __name__ == "__main__":
    agg = JobAggregator()
    agg.run_all()
