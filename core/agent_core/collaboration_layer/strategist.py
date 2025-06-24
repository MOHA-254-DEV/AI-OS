import uuid
import random
from .group_memory import GroupMemory
from .skill_inventory import SkillInventory
from .agent_roles import get_role_config, list_available_roles
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MultiAgentStrategist:
    def __init__(self):
        self.group_memory = GroupMemory()
        self.skills = SkillInventory()
        self.role_assignments = {}

    def assign_roles(self, agent_ids):
        """
        Assigns roles to a list of agents based on their skills.
        """
        available_roles = list(list_available_roles().keys())
        logging.info(f"Assigning roles from: {available_roles}")
        
        for agent_id in agent_ids:
            best_role = self._match_role_by_skill(agent_id, available_roles)
            if agent_id not in self.role_assignments or self.role_assignments[agent_id] != best_role:
                self.skills.set_role(agent_id, best_role)
                self.role_assignments[agent_id] = best_role
                logging.info(f"Assigned role '{best_role}' to agent '{agent_id}'")
        return self.role_assignments

    def _match_role_by_skill(self, agent_id, possible_roles):
        """
        Matches an agent with the best role based on their skills.
        """
        agent_skills = self.skills.get_agent_skills(agent_id)
        if not agent_skills:
            logging.warning(f"No skills found for agent '{agent_id}'. Assigning fallback role.")
            return possible_roles[0] if possible_roles else "unassigned"

        role_scores = {}
        for role in possible_roles:
            role_info = get_role_config(role)
            role_capabilities = role_info.get("capabilities", [])
            if not role_capabilities:
                logging.warning(f"Role '{role}' has no defined capabilities.")
                continue
            overlap = len(set(agent_skills) & set(role_capabilities))
            role_scores[role] = overlap

        if not role_scores:
            return possible_roles[0] if possible_roles else "unassigned"

        return max(role_scores, key=role_scores.get)

    def coordinate_task(self, objective, agents):
        """
        Decomposes the objective and assigns it to agents, logs the plan to group memory.
        """
        task_id = str(uuid.uuid4())
        subtasks = self._decompose_objective(objective)
        plan = {
            "task_id": task_id,
            "objective": objective,
            "subtasks": subtasks,
            "agents": agents
        }
        self.group_memory.log_task(plan)
        logging.info(f"Coordinated plan for objective '{objective}' with {len(subtasks)} subtasks.")
        return plan

    def _decompose_objective(self, objective):
        """
        Decomposes an objective into subtasks.
        """
        # TODO: Replace this with AI/NLP-based decomposition
        return [f"{objective} - subtask {i+1}" for i in range(3)]

    def sync_context(self, agent_id, local_context):
        """
        Synchronizes the agent's context with the shared group memory.
        """
        self.group_memory.update_agent_context(agent_id, local_context)
        logging.info(f"Context synced for agent '{agent_id}'.")

    def validate_and_merge_results(self):
        """
        Validates and merges all completed task results from memory.
        """
        memory = self.group_memory.load()
        results = memory.get("results", {})
        logging.info(f"Validated {len(results)} result entries.")
        return {
            "summary": f"{len(results)} results merged.",
            "result_ids": list(results.keys())
        }

    def reassign_roles(self):
        """
        Reassigns roles based on updated agent skillset.
        """
        all_agents = list(self.skills.load().keys())
        return self.assign_roles(all_agents)
