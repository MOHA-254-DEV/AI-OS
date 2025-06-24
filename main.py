import asyncio
from core.task_scheduler import TaskScheduler

async def main():
    scheduler = TaskScheduler()
    await scheduler.initialize()

    result = await scheduler.run_task(\"echo\", \"hello world\")
    print(result)

    plugin_result = await scheduler.run_task(\"custom_echo\", \"plugin test\")
    print(plugin_result)

if __name__ == '__main__':
    asyncio.run(main())
