import subprocess
import json

class NodeRuntime:
    def run(self, path, args):
        try:
            input_data = json.dumps(args)
            result = subprocess.run(["node", path], input=input_data.encode(),
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            if result.returncode != 0:
                return f"[NODE ERROR] {result.stderr.decode()}"
            return result.stdout.decode()
        except Exception as e:
            return f"[NODE EXEC ERROR] {e}"
