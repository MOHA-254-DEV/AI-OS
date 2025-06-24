import re
import os

class PluginUtils:
    def __init__(self):
        self.restricted_patterns = [
            r'os\.system',
            r'subprocess\.',
            r'eval\(',
            r'exec\(',
            r'open\(.+, [\'\"]w[\'\"]\)',
            r'del ',
            r'rm -rf',
            r'import (os|sys|shutil|ctypes|socket)'
        ]

    def scan_code(self, code: str):
        warnings = []
        for pattern in self.restricted_patterns:
            if re.search(pattern, code):
                warnings.append(f"[SECURITY] Suspicious pattern detected: {pattern}")
        return warnings

    def read_plugin_file(self, path: str) -> str:
        with open(path, 'r') as f:
            return f.read()

    def audit_plugin(self, path: str):
        print(f"[AUDIT] Scanning plugin: {path}")
        code = self.read_plugin_file(path)
        return self.scan_code(code)

if __name__ == "__main__":
    scanner = PluginUtils()
    report = scanner.audit_plugin("plugins/test_plugin.py")
    print("\n".join(report) if report else "Plugin clean.")
