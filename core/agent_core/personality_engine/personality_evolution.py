import os
import json
import random
import logging

class PersonalityEvolutionEngine:
    def __init__(self, profile_dir="profiles/"):
        self.profile_dir = profile_dir
        os.makedirs(self.profile_dir, exist_ok=True)

        self.logger = logging.getLogger("PersonalityEvolution")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def default_profile(self):
        return {
            "curiosity": 0.5,
            "verbosity": 0.5,
            "adaptability": 0.5,
            "empathy": 0.5,
            "communication_style": "balanced",
            "patience": 0.5,
            "humor": 0.5,
            "risk_tolerance": 0.5
        }

    def load_profile(self, agent_id):
        path = os.path.join(self.profile_dir, f"{agent_id}.json")
        if not os.path.exists(path):
            self.logger.warning(f"No profile found for agent {agent_id}. Initializing default.")
            return self.default_profile()

        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load profile for {agent_id}: {e}")
            return self.default_profile()

    def save_profile(self, agent_id, profile):
        path = os.path.join(self.profile_dir, f"{agent_id}.json")
        try:
            with open(path, 'w') as f:
                json.dump(profile, f, indent=4)
            self.logger.info(f"Profile saved for agent {agent_id}")
        except Exception as e:
            self.logger.error(f"Failed to save profile for {agent_id}: {e}")

    def evolve_profile(self, agent_id, feedback_data):
        profile = self.load_profile(agent_id)
        self.logger.info(f"Evolving profile for agent {agent_id} based on feedback: {feedback_data}")

        adjustments = self._compute_adjustments(feedback_data)

        for trait, delta in adjustments.items():
            if trait in profile:
                profile[trait] = round(min(1.0, max(0.0, profile[trait] + delta)), 3)
                self.logger.debug(f"{trait} adjusted by {delta:.3f} to {profile[trait]:.3f}")

        if feedback_data.get("style_preference"):
            self._adjust_communication_style(profile, feedback_data["style_preference"])

        self.save_profile(agent_id, profile)
        return profile

    def _compute_adjustments(self, feedback):
        adjustments = {}
        satisfaction = feedback.get("satisfaction", 0.5)

        if satisfaction > 0.6:
            adjustments.update({
                "curiosity": random.uniform(0.01, 0.05),
                "empathy": random.uniform(0.01, 0.03),
                "patience": random.uniform(0.01, 0.02),
                "humor": random.uniform(0.01, 0.02),
            })
        elif satisfaction < 0.4:
            adjustments.update({
                "verbosity": -random.uniform(0.01, 0.05),
                "adaptability": -random.uniform(0.01, 0.03),
                "risk_tolerance": -random.uniform(0.01, 0.02),
            })
        else:
            adjustments.update({
                "adaptability": random.uniform(-0.01, 0.01),
                "risk_tolerance": random.uniform(-0.01, 0.01),
            })

        return adjustments

    def _adjust_communication_style(self, profile, style_preference):
        valid_styles = ["concise", "verbose", "empathetic", "balanced"]
        if style_preference in valid_styles:
            self.logger.info(f"Updating communication style to '{style_preference}'")
            profile["communication_style"] = style_preference
        else:
            self.logger.warning(f"Unknown communication style '{style_preference}'. Keeping current.")

# === Example usage ===
if __name__ == "__main__":
    engine = PersonalityEvolutionEngine()

    # Simulated feedback
    feedback = {
        "satisfaction": 0.85,
        "style_preference": "concise"
    }

    updated_profile = engine.evolve_profile("agent_42", feedback)
    print("Updated Profile:")
    print(json.dumps(updated_profile, indent=2))
