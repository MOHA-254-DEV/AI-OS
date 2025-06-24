import json
import random

PROFILE_PATH = "data/jobs/user_profile.json"
CACHE_PATH = "data/jobs/job_cache.json"

class AutoApplier:
    def __init__(self):
        self.profile = self.load_profile()
        with open(CACHE_PATH, "r") as f:
            self.jobs = json.load(f)

    def load_profile(self):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)

    def generate_proposal(self, job):
        template = self.profile["template"]
        return template.replace("{job_title}", job["title"]).replace("{skill}", job["category"])

    def apply_to_jobs(self, max_apply=5):
        applied = []
        for job in self.jobs[:max_apply]:
            proposal = self.generate_proposal(job)
            print(f"[APPLYING] {job['title']} on {job['platform']}")
            print(">>> Proposal:\n", proposal)
            applied.append({
                "title": job["title"],
                "platform": job["platform"],
                "proposal": proposal
            })
        return applied

if __name__ == "__main__":
    app = AutoApplier()
    app.apply_to_jobs()
