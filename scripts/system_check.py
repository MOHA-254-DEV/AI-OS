
#!/usr/bin/env python3
"""
System Check Script - Validates entire AI OS for deployment readiness
"""

import os
import sys
import subprocess
import importlib
import json
from pathlib import Path
from typing import List, Dict, Tuple

class SystemChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed_checks = []
        
    def log_error(self, message: str):
        self.errors.append(f"❌ {message}")
        
    def log_warning(self, message: str):
        self.warnings.append(f"⚠️  {message}")
        
    def log_success(self, message: str):
        self.passed_checks.append(f"✅ {message}")

    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major == 3 and version.minor >= 9:
            self.log_success(f"Python {version.major}.{version.minor}.{version.micro}")
            return True
        else:
            self.log_error(f"Python version {version.major}.{version.minor} not supported. Requires Python 3.9+")
            return False

    def check_required_files(self) -> bool:
        """Check if all required files exist"""
        required_files = [
            "main.py",
            "requirements.txt",
            "core/kernel.py",
            "core/task_scheduler.py",
            "api/server.py",
            "utils/logger.py",
            "utils/config.py"
        ]
        
        all_present = True
        for file in required_files:
            if os.path.exists(file):
                self.log_success(f"Required file: {file}")
            else:
                self.log_error(f"Missing required file: {file}")
                all_present = False
                
        return all_present

    def check_dependencies(self) -> bool:
        """Check if all dependencies can be imported"""
        critical_deps = [
            "flask",
            "transformers", 
            "torch",
            "numpy",
            "requests",
            "cryptography",
            "pydantic"
        ]
        
        failed_imports = []
        for dep in critical_deps:
            try:
                importlib.import_module(dep)
                self.log_success(f"Dependency: {dep}")
            except ImportError:
                failed_imports.append(dep)
                self.log_error(f"Missing dependency: {dep}")
                
        return len(failed_imports) == 0

    def check_file_syntax(self) -> bool:
        """Check Python files for syntax errors"""
        python_files = []
        for root, dirs, files in os.walk("."):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        syntax_errors = []
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    compile(f.read(), file, 'exec')
                self.log_success(f"Syntax check: {file}")
            except SyntaxError as e:
                syntax_errors.append(f"{file}: {e}")
                self.log_error(f"Syntax error in {file}: {e}")
            except Exception as e:
                self.log_warning(f"Could not check {file}: {e}")
                
        return len(syntax_errors) == 0

    def check_port_availability(self) -> bool:
        """Check if default ports are available"""
        import socket
        
        ports_to_check = [8000, 5000, 3000]
        available_ports = []
        
        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('0.0.0.0', port))
                available_ports.append(port)
                self.log_success(f"Port {port} available")
            except OSError:
                self.log_warning(f"Port {port} in use")
            finally:
                sock.close()
                
        return len(available_ports) > 0

    def check_deployment_configs(self) -> bool:
        """Check deployment configuration files"""
        deployment_files = [
            "Dockerfile",
            "render.yaml", 
            "railway.json",
            "Procfile",
            "fly.toml",
            ".replit"
        ]
        
        configs_present = 0
        for file in deployment_files:
            if os.path.exists(file):
                configs_present += 1
                self.log_success(f"Deployment config: {file}")
            else:
                self.log_warning(f"Missing deployment config: {file}")
                
        if configs_present >= 3:
            return True
        else:
            self.log_error("Insufficient deployment configurations")
            return False

    def check_environment_variables(self) -> bool:
        """Check for required environment variables"""
        recommended_env_vars = [
            "FLASK_ENV",
            "PORT", 
            "HOST"
        ]
        
        missing_vars = []
        for var in recommended_env_vars:
            if os.getenv(var):
                self.log_success(f"Environment variable: {var}")
            else:
                missing_vars.append(var)
                self.log_warning(f"Missing environment variable: {var}")
                
        return True  # Not critical, just warnings

    def check_security_files(self) -> bool:
        """Check security-related files"""
        security_files = [
            "security/auth.py",
            "security/encryption.py", 
            "security/sandbox.py",
            ".env.example"
        ]
        
        security_present = 0
        for file in security_files:
            if os.path.exists(file):
                security_present += 1
                self.log_success(f"Security file: {file}")
            else:
                self.log_warning(f"Missing security file: {file}")
                
        if security_present >= 2:
            return True
        else:
            self.log_error("Insufficient security configurations")
            return False

    def run_all_checks(self) -> bool:
        """Run all system checks"""
        print("🔍 Running comprehensive system checks...\n")
        
        checks = [
            ("Python Version", self.check_python_version),
            ("Required Files", self.check_required_files),
            ("Dependencies", self.check_dependencies),
            ("File Syntax", self.check_file_syntax),
            ("Port Availability", self.check_port_availability),
            ("Deployment Configs", self.check_deployment_configs),
            ("Environment Variables", self.check_environment_variables),
            ("Security Files", self.check_security_files)
        ]
        
        results = {}
        for name, check_func in checks:
            print(f"Checking {name}...")
            results[name] = check_func()
            print()
            
        return self.generate_report(results)

    def generate_report(self, results: Dict[str, bool]) -> bool:
        """Generate final report"""
        print("=" * 60)
        print("🔍 SYSTEM CHECK REPORT")
        print("=" * 60)
        
        print("\n✅ PASSED CHECKS:")
        for check in self.passed_checks:
            print(f"  {check}")
            
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
                
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
                
        print("\n" + "=" * 60)
        
        failed_checks = sum(1 for result in results.values() if not result)
        total_checks = len(results)
        passed_checks = total_checks - failed_checks
        
        print(f"📊 SUMMARY: {passed_checks}/{total_checks} checks passed")
        
        if failed_checks == 0:
            print("🎉 ALL CHECKS PASSED - System ready for deployment!")
            return True
        elif failed_checks <= 2:
            print("⚠️  MINOR ISSUES - System deployable with warnings")
            return True
        else:
            print("❌ CRITICAL ISSUES - Fix errors before deployment")
            return False

def main():
    checker = SystemChecker()
    success = checker.run_all_checks()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
