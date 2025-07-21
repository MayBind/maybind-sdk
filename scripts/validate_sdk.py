#!/usr/bin/env python3
"""
Validation script for MayBind SDK.
This script validates the generated SDK files and runs basic tests.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def print_status(message):
    """Print status message."""
    print(f"[INFO] {message}")


def print_error(message):
    """Print error message."""
    print(f"[ERROR] {message}")


def print_warning(message):
    """Print warning message."""
    print(f"[WARNING] {message}")


def validate_file_structure():
    """Validate that all required files and directories exist."""
    print_status("Validating file structure...")
    
    required_paths = [
        "openapi/maybind-api.yaml",
        "sdk/python",
        "sdk/python/examples",
        "sdk/python/tests",
        "docs",
        "README.md",
        "LICENSE"
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        print_error(f"Missing required paths: {', '.join(missing_paths)}")
        return False
    
    print_status("File structure validation passed")
    return True


def validate_python_sdk():
    """Validate Python SDK structure."""
    print_status("Validating Python SDK...")
    
    python_sdk_path = Path("sdk/python")
    if not python_sdk_path.exists():
        print_error("Python SDK directory not found")
        return False
    
    # Check for key Python files
    expected_files = [
        "setup.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file in expected_files:
        file_path = python_sdk_path / file
        if not file_path.exists():
            missing_files.append(file)
    
    if missing_files:
        print_warning(f"Missing Python SDK files: {', '.join(missing_files)}")
    
    # Check for Python package structure
    openapi_client_path = python_sdk_path / "openapi_client"
    if openapi_client_path.exists():
        print_status("Python OpenAPI client package found")
    else:
        print_warning("Python OpenAPI client package not found")
    
    return True


def validate_javascript_sdk():
    """Validate JavaScript SDK structure."""
    print_status("Validating JavaScript SDK...")
    
    js_sdk_path = Path("sdk/javascript")
    if not js_sdk_path.exists():
        print_warning("JavaScript SDK directory not found (will be created when needed)")
        return True  # Not an error since we haven't generated it yet
    
    # Check for key JavaScript files
    expected_files = [
        "package.json",
        "README.md"
    ]
    
    missing_files = []
    for file in expected_files:
        file_path = js_sdk_path / file
        if not file_path.exists():
            missing_files.append(file)
    
    if missing_files:
        print_warning(f"Missing JavaScript SDK files: {', '.join(missing_files)}")
    
    # Check package.json structure
    package_json_path = js_sdk_path / "package.json"
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                if 'name' in package_data:
                    print_status(f"JavaScript package name: {package_data['name']}")
                if 'version' in package_data:
                    print_status(f"JavaScript package version: {package_data['version']}")
        except Exception as e:
            print_warning(f"Could not parse package.json: {e}")
    
    return True


def run_python_tests():
    """Run Python tests."""
    print_status("Running Python tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            cwd="sdk/python"
        )
        
        if result.returncode == 0:
            print_status("Python tests passed")
            return True
        else:
            print_warning("Python tests failed or had warnings")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print_warning("pytest not found. Install with: pip install pytest")
        return False
    except Exception as e:
        print_error(f"Error running Python tests: {e}")
        return False


def validate_examples():
    """Validate example files."""
    print_status("Validating example files...")
    
    example_files = [
        "sdk/python/examples/example_chat.py",
        "sdk/python/examples/example_auth_generated.py"
    ]
    
    for example_file in example_files:
        if os.path.exists(example_file):
            print_status(f"Found example: {example_file}")
        else:
            print_warning(f"Missing example: {example_file}")
    
    return True


def main():
    """Main validation function."""
    print("MayBind SDK Validation")
    print("=" * 30)
    
    validation_results = []
    
    # Run validations
    validation_results.append(validate_file_structure())
    validation_results.append(validate_python_sdk())
    validation_results.append(validate_javascript_sdk())
    validation_results.append(validate_examples())
    
    # Run tests (optional)
    print("\n" + "=" * 30)
    print("Running Tests")
    print("=" * 30)
    
    test_results = []
    test_results.append(run_python_tests())
    
    # Summary
    print("\n" + "=" * 30)
    print("Validation Summary")
    print("=" * 30)
    
    passed_validations = sum(validation_results)
    total_validations = len(validation_results)
    
    print(f"Validations passed: {passed_validations}/{total_validations}")
    
    if test_results:
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if all(validation_results):
        print_status("All validations passed!")
        return 0
    else:
        print_error("Some validations failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
