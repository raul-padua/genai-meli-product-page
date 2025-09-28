#!/usr/bin/env python3
"""
Test runner script for the MercadoLibre GenAI evaluation backend.

This script provides various options for running tests:
- All tests
- Unit tests only
- Integration tests only
- Specific test modules
- Coverage reporting
"""

import subprocess
import sys
import os
import argparse


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed!")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Run tests for the backend")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--module", "-m", help="Run specific test module (e.g., test_api)")
    parser.add_argument("--function", "-f", help="Run specific test function")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies")
    
    args = parser.parse_args()
    
    # Change to the backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Install dependencies if requested
    if args.install_deps:
        print("📦 Installing test dependencies...")
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        if not run_command(cmd, "Installing dependencies"):
            sys.exit(1)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-vv")
    else:
        cmd.append("-v")
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=main", "--cov=rag", "--cov-report=html", "--cov-report=term"])
    
    # Add markers for specific test types
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    
    # Add specific module or function
    if args.module:
        cmd.append(f"tests/{args.module}.py")
    elif args.function:
        cmd.extend(["-k", args.function])
    else:
        cmd.append("tests/")
    
    # Run the tests
    success = run_command(cmd, "Running tests")
    
    if args.coverage and success:
        print("\n📊 Coverage report generated in htmlcov/index.html")
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
