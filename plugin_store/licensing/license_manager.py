import hashlib
import time
import uuid

class LicenseManager:
    def __init__(self, license_db_path='plugin_store/licensing/licenses.json'):
        self.db_path = license_db_path
        self._load()

    def _load(self):
        try:
            import json
            with open(self.db_path, 'r') as f:
                self.licenses = json.load(f)
        except FileNotFoundError:
            self.licenses = {}

    def _save(self):
        import json
        with open(self.db_path, 'w') as f:
            json.dump(self.licenses, f, indent=2)

    def generate_license_key(self, plugin_id, user_email, license_type='trial'):
        seed = f"{plugin_id}:{user_email}:{str(uuid.uuid4())}:{time.time()}"
        key = hashlib.sha256(seed.encode()).hexdigest()[:32]
        self.licenses[key] = {
            "plugin_id": plugin_id,
            "user_email": user_email,
            "type": license_type,
            "issued_at": time.time(),
            "valid": True
        }
        self._save()
        return key

    def validate_license_key(self, license_key):
        data = self.licenses.get(license_key, None)
        if data and data["valid"]:
            return True, data
        return False, None

    def revoke_license(self, license_key):
        if license_key in self.licenses:
            self.licenses[license_key]["valid"] = False
            self._save()
            return True
        return False
import json
import os
import hashlib
import time
from plugin_store.licensing.plan_limits import PlanLimits

LICENSE_STORE = "plugin_store/licensing/license_store.json"

class LicenseManager:
    def __init__(self):
        self.license_store = LICENSE_STORE
        self.plan_limits = PlanLimits()
        self._load_licenses()

    def _load_licenses(self):
        if not os.path.exists(self.license_store):
            with open(self.license_store, 'w') as f:
                json.dump({}, f)
        with open(self.license_store, 'r') as f:
            self.licenses = json.load(f)

    def _save_licenses(self):
        with open(self.license_store, 'w') as f:
            json.dump(self.licenses, f, indent=2)

    def _hash_key(self, key):
        return hashlib.sha256(key.encode()).hexdigest()

    def activate_license(self, plugin_id, license_key, plan='basic', expiry_days=30):
        license_hash = self._hash_key(license_key)
        expiry = time.time() + expiry_days * 86400
        self.licenses[plugin_id] = {
            "key": license_hash,
            "plan": plan,
            "usage": {},
            "expires_at": expiry
        }
        self._save_licenses()
        print(f"✅ License activated for plugin '{plugin_id}' with plan '{plan}'.")

    def validate_license(self, plugin_id, license_key):
        if plugin_id not in self.licenses:
            return False, "🔒 License not found."

        license_data = self.licenses[plugin_id]
        if time.time() > license_data['expires_at']:
            return False, "❌ License expired."

        if self._hash_key(license_key) != license_data['key']:
            return False, "❌ Invalid license key."

        return True, license_data['plan']

    def track_usage(self, plugin_id, user_id):
        if plugin_id not in self.licenses:
            raise Exception("🔒 Plugin not licensed.")

        license_data = self.licenses[plugin_id]
        plan = license_data["plan"]

        # Check expiry
        if time.time() > license_data['expires_at']:
            raise Exception("❌ License expired.")

        # Track usage
        if user_id not in license_data["usage"]:
            license_data["usage"][user_id] = {"count": 0, "last_reset": time.time()}
        usage = license_data["usage"][user_id]

        # Reset count daily
        if time.time() - usage["last_reset"] > 86400:
            usage["count"] = 0
            usage["last_reset"] = time.time()

        usage["count"] += 1
        self._save_licenses()

        limit = self.plan_limits.get_limit(plan)
        if usage["count"] > limit:
            raise Exception(f"🚫 Daily limit reached for plan '{plan}'.")

    def revoke_license(self, plugin_id):
        if plugin_id in self.licenses:
            del self.licenses[plugin_id]
            self._save_licenses()
            print(f"❎ License revoked for plugin '{plugin_id}'.")
