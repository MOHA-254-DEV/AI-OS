import asyncio
import heapq
from task_engine.job_model import Job

class PriorityQueue:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.heap = []

    async def add_job(self, job: Job):
        async with self.lock:
            heapq.heappush(self.heap, (job.priority, job.created_at, job))

    async def get_next_job(self) -> Job:
        async with self.lock:
            if not self.heap:
                return None
            return heapq.heappop(self.heap)[2]

    async def all_jobs(self):
        async with self.lock:
            return [j[2] for j in self.heap]
