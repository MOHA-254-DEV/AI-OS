import yaml
from typing import Dict, List, Optional, Any


class RoleManager:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.roles = config["roles"] if config and "roles" in config else self._default_roles()

    def _default_roles(self) -> Dict[str, Dict[str, Any]]:
        return {
            "Developer": {
                "skills": ["python", "javascript", "git"],
                "capabilities": ["code_generation", "debug", "optimize"],
                "priority": 10
            },
            "Designer": {
                "skills": ["photoshop", "figma", "illustration"],
                "capabilities": ["ui_mockup", "graphic_editing"],
                "priority": 7
            },
            "DataSpecialist": {
                "skills": ["excel", "sql", "pandas"],
                "capabilities": ["data_entry", "cleaning", "analysis"],
                "priority": 8
            },
            "Marketer": {
                "skills": ["seo", "email", "copywriting"],
                "capabilities": ["campaign_run", "ad_analysis", "content_generation"],
                "priority": 6
            },
            "BusinessStrategist": {
                "skills": ["finance", "projections", "strategy"],
                "capabilities": ["plan_evaluation", "risk_assessment"],
                "priority": 5
            }
        }

    def load_from_yaml(self, yaml_str: str):
        try:
            parsed = yaml.safe_load(yaml_str)
            if isinstance(parsed, dict) and "roles" in parsed:
                self.roles = parsed["roles"]
            else:
                raise ValueError("YAML must contain a top-level 'roles' key.")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parse error: {str(e)}")

    def load_from_yaml_file(self, filepath: str):
        with open(filepath, "r") as file:
            self.load_from_yaml(file.read())

    def get_role_info(self, role_name: str) -> Optional[Dict[str, Any]]:
        return self.roles.get(role_name)

    def get_roles(self) -> List[str]:
        return list(self.roles.keys())

    def get_skills(self, role_name: str) -> List[str]:
        return self.roles.get(role_name, {}).get("skills", [])

    def get_capabilities(self, role_name: str) -> List[str]:
        return self.roles.get(role_name, {}).get("capabilities", [])

    def get_priority(self, role_name: str) -> int:
        return self.roles.get(role_name, {}).get("priority", 0)

    def add_role(self, role_name: str, skills: List[str], capabilities: List[str], priority: int = 1):
        self.roles[role_name] = {
            "skills": skills,
            "capabilities": capabilities,
            "priority": priority
        }

    def update_role(self, role_name: str, skills: Optional[List[str]] = None,
                    capabilities: Optional[List[str]] = None, priority: Optional[int] = None):
        if role_name not in self.roles:
            raise ValueError(f"Role '{role_name}' does not exist.")
        if skills is not None:
            self.roles[role_name]["skills"] = skills
        if capabilities is not None:
            self.roles[role_name]["capabilities"] = capabilities
        if priority is not None:
            self.roles[role_name]["priority"] = priority

    def remove_role(self, role_name: str):
        if role_name in self.roles:
            del self.roles[role_name]

    def find_best_role_for_task(self, task_description: str) -> str:
        tokens = task_description.lower().split()
        role_scores = {}

        for role, props in self.roles.items():
            score = sum(
                1 for cap in props.get("capabilities", [])
                if any(cap.lower() in token or token in cap.lower() for token in tokens)
            )
            if score > 0:
                role_scores[role] = score

        if not role_scores:
            # fallback: return highest priority role
            return max(self.roles.items(), key=lambda r: r[1].get("priority", 0))[0]

        sorted_roles = sorted(
            role_scores.items(),
            key=lambda x: (x[1], self.get_priority(x[0])),
            reverse=True
        )
        return sorted_roles[0][0]

    def filter_roles_by_skill(self, skill: str) -> List[str]:
        return [role for role, props in self.roles.items()
                if skill.lower() in [s.lower() for s in props.get("skills", [])]]

    def filter_roles_by_capability(self, capability: str) -> List[str]:
        return [role for role, props in self.roles.items()
                if capability.lower() in [c.lower() for c in props.get("capabilities", [])]]
