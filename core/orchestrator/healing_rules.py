# File: core/orchestrator/healing_rules.py

from typing import Dict


class HealingRules:
    _rules: Dict[str, Dict[str, str | int]] = {
        "CPUOverload": {
            "action": "restart_agent",
            "threshold": 90,
            "severity": "medium"
        },
        "MemoryLeak": {
            "action": "restart_agent",
            "threshold": 100,
            "severity": "high"
        },
        "PluginCrash": {
            "action": "rebuild_dependencies",
            "severity": "critical"
        },
        "IOFailure": {
            "action": "reroute_task",
            "severity": "low"
        },
        "HeartbeatLost": {
            "action": "alert_admin",
            "severity": "critical"
        }
    }

    @classmethod
    def get_action(cls, fault_type: str) -> Dict[str, str | int]:
        """
        Get the healing action and severity for a given fault type.
        """
        return cls._rules.get(fault_type, {
            "action": "log_only",
            "severity": "unknown"
        })

    @classmethod
    def add_rule(cls, fault_type: str, action: str, severity: str, threshold: int = None):
        """
        Dynamically add or update a fault handling rule.
        """
        rule = {
            "action": action,
            "severity": severity
        }
        if threshold is not None:
            rule["threshold"] = threshold
        cls._rules[fault_type] = rule

    @classmethod
    def all_rules(cls) -> Dict[str, Dict[str, str | int]]:
        """
        Return all current healing rules.
        """
        return cls._rules.copy()
