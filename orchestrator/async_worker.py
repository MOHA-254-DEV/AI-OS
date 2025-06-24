import asyncio
import concurrent.futures

def run_task_async(task, executor):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(run(task, executor))

async def run(task, executor):
    try:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await asyncio.get_event_loop().run_in_executor(
                pool, lambda: executor.execute(task.plugin["entry"], 
                                               runtime=task.plugin["runtime"], 
                                               args=task.args)
            )
            return {"status": "success", "output": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
