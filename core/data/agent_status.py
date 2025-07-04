
import json

data = {
    "agents": [
        {"id": "agent1", "cpu": 45, "memory": 512, "queue": 5},
        {"id": "agent2", "cpu": 95, "memory": 900, "queue": 10}
    ]
}

def analyze_agent_health(agents):
    overloaded = []
    for agent in agents:
        if agent["cpu"] > 90 or agent["memory"] > 800 or agent["queue"] > 8:
            overloaded.append({
                "id": agent["id"],
                "issues": {
                    "high_cpu": agent["cpu"] > 90,
                    "high_memory": agent["memory"] > 800,
                    "high_queue": agent["queue"] > 8
                }
            })
    return overloaded

if __name__ == "__main__":
    alerts = analyze_agent_health(data["agents"])
    print("Overloaded Agents:", json.dumps(alerts, indent=2))
