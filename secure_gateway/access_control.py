class AccessControl:
    def __init__(self):
        self.policies = {
            "admin": {"can_generate_report": True, "can_deploy": True, "can_manage_tokens": True},
            "user": {"can_generate_report": True, "can_deploy": False, "can_manage_tokens": False},
            "guest": {"can_generate_report": False, "can_deploy": False, "can_manage_tokens": False}
        }

    def check_permission(self, role, permission):
        if role not in self.policies:
            return False
        return self.policies[role].get(permission, False)

if __name__ == "__main__":
    ac = AccessControl()
    print("Admin deploy:", ac.check_permission("admin", "can_deploy"))
    print("User deploy:", ac.check_permission("user", "can_deploy"))
