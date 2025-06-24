import json
import os
import logging
from .personality_traits import AGENT_TRAITS

class PersonalityProfileManager:
    def __init__(self, profile_dir="profiles/", default_type="default"):
        self.traits = AGENT_TRAITS
        self.default_type = default_type
        self.profile_dir = profile_dir
        os.makedirs(self.profile_dir, exist_ok=True)

        self.logger = logging.getLogger("ProfileManager")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def get_profile(self, agent_id=None, profile_type=None):
        selected_type = profile_type or self.default_type
        if agent_id:
            profile = self.load_profile(agent_id)
            if profile:
                return profile
            else:
                self.logger.warning(f"No profile found for agent '{agent_id}'. Using default.")
        return self.traits.get(selected_type, self.traits[self.default_type])

    def load_profile(self, agent_id):
        path = os.path.join(self.profile_dir, f"{agent_id}.json")
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    profile = json.load(f)
                    self.logger.info(f"Loaded profile for agent: {agent_id}")
                    return profile
        except json.JSONDecodeError:
            self.logger.error(f"Corrupted profile file for agent: {agent_id}")
        return None

    def save_profile(self, agent_id, profile):
        path = os.path.join(self.profile_dir, f"{agent_id}.json")
        try:
            with open(path, 'w') as f:
                json.dump(profile, f, indent=4)
            self.logger.info(f"Saved profile for agent: {agent_id}")
        except Exception as e:
            self.logger.error(f"Error saving profile for {agent_id}: {e}")

    def customize_profile(self, base_type, overrides):
        base = self.traits.get(base_type, self.traits[self.default_type]).copy()
        merged = {**base, **overrides}
        self.logger.info(f"Customized profile from base '{base_type}' with overrides.")
        return merged

    def reset_profile(self, agent_id):
        default_profile = self.traits.get(self.default_type, self.traits["default"])
        self.save_profile(agent_id, default_profile)
        self.logger.info(f"Reset profile for agent: {agent_id}")
        return default_profile

    def merge_profiles(self, base_profile, override_profile):
        merged = {**base_profile, **override_profile}
        self.logger.debug("Merged base and override profiles.")
        return merged

    def validate_profile(self, profile):
        """
        Ensure all float traits are within range [0.0, 1.0]
        """
        validated = {}
        for key, value in profile.items():
            if isinstance(value, float):
                validated[key] = max(0.0, min(1.0, value))
            else:
                validated[key] = value
        return validated
