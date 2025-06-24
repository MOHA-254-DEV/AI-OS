import builtins

SAFE_BUILTINS = {
    "abs": abs, "all": all, "any": any,
    "bool": bool, "dict": dict, "float": float,
    "int": int, "len": len, "list": list, "max": max,
    "min": min, "range": range, "str": str, "sum": sum,
    "print": print
}

class SafeExec:
    def __init__(self):
        self.globals = {"__builtins__": SAFE_BUILTINS}
        self.locals = {}

    def execute(self, code: str):
        try:
            exec(code, self.globals, self.locals)
        except Exception as e:
            print("[SANDBOX ERROR]", e)

if __name__ == "__main__":
    sandbox = SafeExec()
    while True:
        code = input(">>> ")
        if code.strip().lower() == "exit":
            break
        sandbox.execute(code)
