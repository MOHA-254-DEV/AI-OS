import subprocess

class BashRuntime:
    def run(self, path, args):
        try:
            cmd = [path] + [f"{k}={v}" for k, v in args.items()]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            if result.returncode != 0:
                return f"[BASH ERROR] {result.stderr.decode()}"
            return result.stdout.decode()
        except Exception as e:
            return f"[BASH EXEC ERROR] {e}"
