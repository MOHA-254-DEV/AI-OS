import os
import json
import random
import logging

class EnhancedPersonalityEvolutionEngine:
    def __init__(self, agent_traits, profile_dir="profiles/"):
        self.agent_traits = agent_traits
        self.profile_dir = profile_dir
        os.makedirs(self.profile_dir, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger("PersonalityEvolution")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def default_profile(self):
        return {
            "name": "Standard",
            "communication_style": "balanced",
            "risk_tolerance": 0.5,
            "collaboration": 0.5,
            "verbosity": 0.5,
            "focus": "generalist",
            "empathy": 0.5,
            "curiosity": 0.5,
            "adaptability": 0.5
        }

    def load_profile(self, agent_id):
        path = os.path.join(self.profile_dir, f"{agent_id}.json")
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    profile = json.load(f)
                    self.logger.info(f"Loaded profile for agent: {agent_id}")
                    return profile
            except Exception as e:
                self.logger.warning(f"Failed to load profile for {agent_id}: {e}")
        self.logger.warning(f"Using default profile for agent: {agent_id}")
        return self.default_profile()

    def save_profile(self, agent_id, profile):
        path = os.path.join(self.profile_dir, f"{agent_id}.json")
        try:
            with open(path, 'w') as f:
                json.dump(profile, f, indent=4)
            self.logger.info(f"Saved updated profile for agent: {agent_id}")
        except Exception as e:
            self.logger.error(f"Error saving profile for {agent_id}: {e}")

    def evolve_profile(self, agent_id, feedback_data):
        profile = self.load_profile(agent_id)
        self.logger.info(f"Applying feedback to agent {agent_id}: {feedback_data}")

        adjustments = self._compute_adjustments(feedback_data)

        for trait, delta in adjustments.items():
            if trait in profile and isinstance(profile[trait], float):
                old_val = profile[trait]
                profile[trait] = round(min(1.0, max(0.0, old_val + delta)), 3)
                self.logger.debug(f"{trait}: {old_val:.2f} -> {profile[trait]:.2f}")

        if feedback_data.get("style_preference"):
            self._adjust_communication_style(profile, feedback_data["style_preference"])

        self.save_profile(agent_id, profile)
        return profile

    def _compute_adjustments(self, feedback):
        adjustments = {}
        score = feedback.get("satisfaction", 0.5)

        if score > 0.6:
            adjustments.update({
                "curiosity": random.uniform(0.01, 0.05),
                "empathy": random.uniform(0.01, 0.03),
                "collaboration": random.uniform(0.01, 0.02)
            })
        elif score < 0.4:
            adjustments.update({
                "verbosity": -random.uniform(0.01, 0.05),
                "risk_tolerance": -random.uniform(0.01, 0.03),
                "adaptability": -random.uniform(0.01, 0.02)
            })
        else:
            adjustments["adaptability"] = random.uniform(-0.01, 0.01)

        return adjustments

    def _adjust_communication_style(self, profile, style_preference):
        valid_styles = ["concise", "expressive", "formal", "empathetic", "balanced"]
        if style_preference.lower() in valid_styles:
            self.logger.info(f"Setting communication style to '{style_preference}'")
            profile["communication_style"] = style_preference.lower()
        else:
            self.logger.warning(f"Invalid style '{style_preference}', defaulting to balanced.")
            profile["communication_style"] = "balanced"

    def create_agent(self, agent_type):
        """
        Create a profile from predefined agent_traits dictionary.
        """
        profile = self.agent_traits.get(agent_type)
        if not profile:
            self.logger.warning(f"No predefined traits found for {agent_type}. Using default.")
            return self.default_profile()

        return profile.copy()
