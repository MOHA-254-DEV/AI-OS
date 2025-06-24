import os
import subprocess
import shutil
import json

class DeployManager:
    def __init__(self):
        self.project_dir = os.getcwd()

    def deploy_to_replit(self):
        print("[DEPLOY] Replit: Setting up .replit and main.py...")
        with open(".replit", "w") as f:
            f.write("run = \"python3 main.py\"")
        if not os.path.exists("main.py"):
            shutil.copy("aios.py", "main.py")
        print("✅ Replit deployment scaffolded. Push to Replit manually or use Git.")

    def deploy_to_vercel(self):
        print("[DEPLOY] Vercel: Creating vercel.json...")
        vercel_config = {
            "version": 2,
            "builds": [{"src": "web/index.html", "use": "@vercel/static"}],
            "routes": [{"src": "/(.*)", "dest": "/web/index.html"}]
        }
        with open("vercel.json", "w") as f:
            json.dump(vercel_config, f, indent=2)
        print("✅ Vercel config created. Run `vercel` to deploy.")

    def deploy_to_github_pages(self, repo_url):
        print("[DEPLOY] GitHub Pages: Initializing repo + pushing...")
        os.system("git init")
        os.system("git remote add origin " + repo_url)
        os.system("git add . && git commit -m 'Initial deploy'")
        os.system("git branch -M main")
        os.system("git push -u origin main")
        os.system("git subtree push --prefix web origin gh-pages")

if __name__ == "__main__":
    deployer = DeployManager()
    deployer.deploy_to_replit()
