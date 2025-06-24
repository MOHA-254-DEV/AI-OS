import os

class VercelDeployer:
    def __init__(self):
        self.project_name = "ai-os-vercel"
        self.vercel_token = os.getenv("VERCEL_TOKEN", "")

    def deploy(self):
        print("[VERCEL] Deploying project...")
        os.system("vercel --prod --yes")

if __name__ == "__main__":
    VercelDeployer().deploy()
