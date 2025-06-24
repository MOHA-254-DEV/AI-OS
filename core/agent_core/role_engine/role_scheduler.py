from typing import List, Optional, Dict, Any, Union


class RoleScheduler:
    def __init__(self, role_manager, verbose: bool = False, weight_priority: float = 1.0, weight_load: float = 1.0):
        """
        Initializes the RoleScheduler with a role manager and optional parameters.

        :param role_manager: A RoleManager instance.
        :param verbose: Whether to print debug information during scheduling.
        :param weight_priority: Multiplier for priority weight.
        :param weight_load: Multiplier for load influence.
        """
        self.role_manager = role_manager
        self.verbose = verbose
        self.weight_priority = weight_priority
        self.weight_load = weight_load

    def assign_role_by_load_and_priority(self, agents: List[Any], task: Dict[str, Any]) -> Optional[Any]:
        """
        Assigns the most suitable agent for a task based on load and role priority.

        :param agents: List of agent-like objects with 'role', 'load', 'name' attributes.
        :param task: A task dictionary with a 'type' or 'description' field.
        :return: The selected agent or None.
        """
        task_type = task.get("type") or task.get("description") or ""
        capable_roles = self.role_manager.get_capable_roles(task_type)
        best_agent = None
        best_score = -1.0

        for agent in agents:
            agent_role = getattr(agent, "role", None)
            agent_load = getattr(agent, "load", 0)
            agent_name = getattr(agent, "name", "Unknown")

            # If agent has no role assigned, infer one from task
            if not agent_role:
                agent_role = self.role_manager.find_best_role_for_task(task_type)

            if agent_role in capable_roles:
                role_priority = self.role_manager.get_priority(agent_role)
                load_factor = 1.0 / (agent_load + 1.0)  # Prevent division by 0
                score = (role_priority * self.weight_priority) * (load_factor * self.weight_load)

                if self.verbose:
                    print(f"[Scheduler] Agent '{agent_name}' with role '{agent_role}' scored {score:.2f}")

                if score > best_score:
                    best_agent = agent
                    best_score = score
                elif score == best_score:
                    # Tie-breaker: lower load wins
                    if agent_load < getattr(best_agent, "load", float('inf')):
                        best_agent = agent

        if self.verbose and best_agent:
            print(f"[Scheduler] Selected Agent: {getattr(best_agent, 'name', 'Unnamed')}")

        return best_agent
