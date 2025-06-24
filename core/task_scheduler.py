import asyncio
from core.plugin_manager import PluginManager

class TaskScheduler:
    def __init__(self):
        self.tasks = {}
        self.plugin_manager = PluginManager()

    async def initialize(self):
        await self.register_task(\"echo\", self.echo_task)
        self.plugin_manager.load_plugins()
        for name, func in self.plugin_manager.plugins.items():
            for task, handler in func.items():
                await self.register_task(task, handler)

    async def register_task(self, task_name, handler):
        self.tasks[task_name] = handler

    async def echo_task(self, data):
        return f\"Echo: {data}\"

    async def run_task(self, task_name, data):
        if task_name in self.tasks:
            return await self.tasks[task_name](data)
        else:
            return f\"Task '{task_name}' not found.\"
