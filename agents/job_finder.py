import os
import json
import aiohttp
import asyncio
from datetime import datetime
from utils.logger import logger, log_task
from typing import List, Dict


class JobFinder:
    def __init__(self, save_file="data/jobs/results.json", retry_limit=3, delay=2):
        self.save_file = save_file
        self.retry_limit = retry_limit
        self.delay = delay
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)

    async def fetch_all_jobs(self, query="python") -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._fetch_with_retry(session, f"https://remotive.io/api/remote-jobs?search={query}", "remotive.io", self._parse_remotive_jobs),
                self._fetch_with_retry(session, "https://remoteok.com/api", "remoteok.com", self._parse_remoteok_jobs, query),
                self._fetch_with_retry(session, f"https://www.freelancer.com/api/projects/0.1/projects/active/?query={query}&compact=true", "freelancer.com", self._parse_freelancer_jobs)
            ]
            return await asyncio.gather(*tasks)

    async def _fetch_with_retry(self, session, url: str, source: str, parser, *args) -> Dict:
        attempt = 0
        while attempt < self.retry_limit:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise aiohttp.ClientError(f"Status code {response.status}")
                    text = await response.text()
                    data = await response.json()
                    jobs = parser(data, *args)
                    self._save_jobs(jobs)
                    logger.info(f"{len(jobs)} jobs fetched from {source}")
                    return {"source": source, "count": len(jobs)}
            except Exception as e:
                attempt += 1
                logger.warning(f"[{source}] Attempt {attempt} failed: {e}")
                await asyncio.sleep(self.delay * attempt)  # exponential backoff
        logger.error(f"❌ Failed to fetch data from {source} after {self.retry_limit} attempts.")
        return {"source": source, "error": "Fetch failed"}

    def _parse_remotive_jobs(self, data, *args):
        jobs = data.get("jobs", [])
        return [job for job in jobs if job.get("job_type") == "Full-Time"]

    def _parse_remoteok_jobs(self, data, query):
        return [
            job for job in data
            if isinstance(job, dict) and query.lower() in job.get("position", "").lower()
        ]

    def _parse_freelancer_jobs(self, data, *args):
        return data.get("result", {}).get("projects", [])

    def _save_jobs(self, jobs: List[Dict]):
        try:
            timestamp = datetime.utcnow().isoformat()
            payload = {"timestamp": timestamp, "jobs": jobs}
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            log_task("job_fetch", "saved", f"{len(jobs)} jobs @ {timestamp}")
        except Exception as e:
            logger.error(f"Failed to save jobs: {e}")

    def list_saved_jobs(self) -> Dict:
        if not os.path.exists(self.save_file):
            return {"error": "No saved jobs found."}
        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading saved jobs: {e}")
            return {"error": "Could not read saved job file."}


# Async Test Execution
if __name__ == "__main__":
    async def main():
        job_finder = JobFinder()
        results = await job_finder.fetch_all_jobs(query="python")
        for res in results:
            print(res)

        saved = job_finder.list_saved_jobs()
        print(f"\nSaved Jobs Snapshot:\n{json.dumps(saved, indent=2)}")

    asyncio.run(main())
