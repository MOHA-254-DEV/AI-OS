import asyncio
from task_engine.queue_engine import PriorityQueue
from task_engine.job_model import JobStatus
import random

class TaskProcessor:
    def __init__(self):
        self.queue = PriorityQueue()
        self.listeners = set()
        self.jobs_by_id = {}
        self.max_retries = 3

    async def register_ws(self, websocket):
        self.listeners.add(websocket)

    async def unregister_ws(self, websocket):
        self.listeners.remove(websocket)

    async def notify_all(self, job):
        for ws in self.listeners.copy():
            try:
                await ws.send_json(job.to_dict())
            except:
                self.listeners.discard(ws)

    async def submit_job(self, job):
        self.jobs_by_id[job.id] = job
        await self.queue.add_job(job)
        await self.notify_all(job)

    async def get_all_jobs(self):
        return [job.to_dict() for job in self.jobs_by_id.values()]

    async def worker_loop(self):
        while True:
            job = await self.queue.get_next_job()
            if job:
                job.status = JobStatus.PROCESSING
                await self.notify_all(job)
                await asyncio.sleep(random.randint(1, 3))  # Simulate task run

                # Random success/failure simulation
                if random.random() < 0.85:
                    job.status = JobStatus.COMPLETED
                    job.result = {"message": "Success"}
                else:
                    job.status = JobStatus.FAILED
                    job.retries += 1
                    if job.retries < self.max_retries:
                        job.status = JobStatus.QUEUED
                        await self.queue.add_job(job)
                    else:
                        job.result = {"message": "Failed after retries"}
                await self.notify_all(job)
            await asyncio.sleep(1)
