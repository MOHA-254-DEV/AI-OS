import re
import json
import logging
import difflib
from core.task_manager import TaskManager

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Planner:
    def __init__(self):
        self.taskman = TaskManager()

        # More extensible structure for matching
        self.command_patterns = {
            "create_invoice": ["invoice", "bill", "receipt"],
            "generate_contract": ["contract", "agreement"],
            "summarize_meeting": ["summary", "summarize", "meeting notes"],
            "compose_email": ["email", "send email", "compose"],
            "simulate_trade": ["trade", "trading", "simulate"],
            "generate_graphic": ["design", "graphic", "image", "illustration"],
            "analyze_seo": ["seo", "search engine", "ranking", "keywords"],
            "deploy_app": ["deploy", "launch app", "release"],
            "run_virtual_assistant": ["assistant", "ai assistant", "virtual agent"],
            "generate_report": ["report", "analytics", "summary report"],
            "generate_product_list": ["product list", "products", "items"],
            "create_shopify_store": ["shopify", "store", "ecommerce"],
            "upload_products": ["upload", "inventory", "catalog"],
            "run_ad_campaign": ["ads", "marketing", "campaign"],
            "transcribe_audio": ["transcribe", "audio", "voice"],
        }

    def _extract_entities(self, text):
        """
        Extract entities including quoted strings and contextual phrases like 'from', 'for', etc.
        """
        quoted = re.findall(r'"(.*?)"', text)
        location = re.findall(r'\bfrom\s+([\w\s]+)', text.lower())
        target = re.findall(r'\bfor\s+([\w\s]+)', text.lower())
        return quoted + location + target

    def _get_command(self, prompt):
        """
        Determine the best command match based on fuzzy keyword search.
        """
        prompt_lower = prompt.lower()
        for command, patterns in self.command_patterns.items():
            for pattern in patterns:
                if pattern in prompt_lower:
                    logger.info(f"Pattern matched for command: {command}")
                    return command

        # Fallback: use difflib fuzzy match
        all_keywords = [kw for pat in self.command_patterns.values() for kw in pat]
        matches = difflib.get_close_matches(prompt_lower, all_keywords, n=1, cutoff=0.6)
        if matches:
            for command, patterns in self.command_patterns.items():
                if matches[0] in patterns:
                    logger.info(f"Fuzzy matched command: {command}")
                    return command

        logger.warning("No command matched for prompt.")
        return None

    def plan_from_prompt(self, prompt):
        """
        Generate a task plan from a natural language prompt.
        """
        logger.info(f"Planning task from prompt: {prompt}")
        command = self._get_command(prompt)
        if not command:
            logger.error("Unable to determine action from prompt.")
            return {"error": "Unable to determine action from prompt."}

        args = self._extract_entities(prompt)
        task = self.taskman.add_task(command, args)
        if not task:
            logger.error("Failed to create task.")
            return {"error": "Failed to create task."}

        logger.info(f"Task created: {task['id']} -> {command}({args})")
        return {
            "prompt": prompt,
            "task_command": command,
            "args": args,
            "task_id": task["id"]
        }

    def generate_task_chain(self, goal_prompt):
        """
        Break down complex prompts into chains of sequential tasks.
        """
        logger.info(f"Generating task chain for: {goal_prompt}")
        tasks = []

        prompt_lower = goal_prompt.lower()

        if "launch" in prompt_lower and "store" in prompt_lower:
            tasks = [
                ("generate_product_list", []),
                ("create_shopify_store", []),
                ("upload_products", []),
                ("run_ad_campaign", [])
            ]
        elif "summarize meeting" in prompt_lower or "meeting summary" in prompt_lower:
            tasks = [
                ("transcribe_audio", []),
                ("summarize_meeting", [])
            ]
        else:
            single_task = self.plan_from_prompt(goal_prompt)
            if "error" in single_task:
                logger.error("Failed to create single task in task chain.")
                return {"error": "Failed to create task chain."}
            tasks.append((single_task["task_command"], single_task["args"]))

        task_ids = []
        for command, args in tasks:
            task = self.taskman.add_task(command, args)
            if task:
                task_ids.append(task["id"])
                logger.info(f"Chained task created: {task['id']} ({command})")
            else:
                logger.error(f"Failed to add task {command} to chain.")

        return {
            "goal": goal_prompt,
            "task_chain": tasks,
            "task_ids": task_ids
        }

    def list_commands(self):
        """
        Return a list of all supported commands and their patterns.
        """
        return self.command_patterns
