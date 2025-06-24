from .trace_logger import TraceLogger
from typing import List, Dict


class ChainOfThoughtSimulator:
    """
    Simulates structured reasoning for an agent working on a task.
    Tracks the thinking process with TraceLogger.
    """

    def __init__(self, agent_id: str, task_id: str):
        if not isinstance(agent_id, str) or not agent_id.strip():
            raise ValueError("Invalid agent_id.")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("Invalid task_id.")
        self.agent_id = agent_id
        self.task_id = task_id
        self.logger = TraceLogger(agent_id, task_id)

    def simulate(self, task_description: str) -> str:
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Invalid task description.")

        self.logger.log_step("🎯 Task received", {"description": task_description})

        tokens = task_description.strip().split()
        self.logger.log_step("🧠 Tokenizing task", {"tokens": tokens})

        concepts = self._classify_concepts(tokens)
        self.logger.log_step("🔍 Classifying concepts", concepts)

        strategy = self._choose_strategy(task_description)
        self.logger.log_step("🧩 Selected reasoning strategy", {"strategy": strategy})

        substeps = self._generate_substeps(concepts)
        self.logger.log_step("🛠 Planning substeps", {"substeps": substeps})

        thought_path = self._simulate_execution(substeps)
        self.logger.log_step("🚀 Simulated reasoning path", {"path": thought_path})

        self.logger.save()
        return "🧠 Chain of thought simulation complete."

    def _classify_concepts(self, tokens: List[str]) -> Dict[str, List[str]]:
        action_words = []
        subject_words = []

        for token in tokens:
            if token.lower() in {"build", "create", "analyze", "optimize", "fetch", "evaluate", "simulate"}:
                action_words.append(token)
            else:
                subject_words.append(token)

        return {
            "actions": action_words,
            "subjects": subject_words
        }

    def _choose_strategy(self, description: str) -> str:
        lowered = description.lower()
        if "analyze" in lowered or "research" in lowered:
            return "deductive reasoning with data validation"
        elif "plan" in lowered or "design" in lowered:
            return "systemic ideation + feasibility check"
        elif "build" in lowered or "code" in lowered:
            return "iterative decomposition + implementation"
        return "default heuristics + feedback loop"

    def _generate_substeps(self, concept_data: Dict[str, List[str]]) -> List[str]:
        base = ["Understand objective", "Clarify constraints"]
        if concept_data["actions"]:
            base += [f"Apply action: {act}" for act in concept_data["actions"]]
        if concept_data["subjects"]:
            base += [f"Contextualize subject: {sub}" for sub in concept_data["subjects"]]
        base.append("Synthesize output")
        return base

    def _simulate_execution(self, substeps: List[str]) -> List[Dict[str, str]]:
        path = []
        for i, step in enumerate(substeps, 1):
            reflection = f"Step-{i}: {step}"
            self.logger.log_step(f"🔄 Executing substep {i}", {"step": step})
            path.append({"step": step, "reflection": reflection})
        return path
