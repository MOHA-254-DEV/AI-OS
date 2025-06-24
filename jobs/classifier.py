import json
import os

from transformers import pipeline
CLASSIFIER = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CATEGORIES = [
    "graphic design", "data entry", "virtual assistant", "dropshipping",
    "software development", "finance", "business", "trading", "web scraping"
]

class JobClassifier:
    def __init__(self, cache_path="data/jobs/job_cache.json"):
        self.cache_path = cache_path
        with open(cache_path, "r") as f:
            self.jobs = json.load(f)

    def classify(self):
        for job in self.jobs:
            text = f"{job['title']} - {job['description']}"
            result = CLASSIFIER(text, CATEGORIES)
            job["category"] = result["labels"][0]
        with open(self.cache_path, "w") as f:
            json.dump(self.jobs, f, indent=4)
        return self.jobs

if __name__ == "__main__":
    clf = JobClassifier()
    print(clf.classify())
