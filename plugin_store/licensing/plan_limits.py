class PlanLimits:
    def __init__(self):
        self.plan_config = {
            "basic": 20,
            "pro": 100,
            "business": 500,
            "enterprise": 10000
        }

    def get_limit(self, plan):
        return self.plan_config.get(plan, 20)
