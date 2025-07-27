#!/usr/bin/env python3
"""
Quick setup for Maybind Python SDK
Checks prerequisites, installs dependencies, and configures the environment.
"""

import os
import sys
import subprocess
import importlib.util
import getpass
from pathlib import Path

def print_header():
    """Print the header"""
    print("🚀 Maybind SDK Quick Setup")
    print("=" * 30)

def check_python_version():
    """Check if Python version meets requirements (3.9+)"""
    print("Checking Python version...")
    
    current_version = sys.version_info
    required_version = (3, 9)
    
    print(f"   Current Python: {current_version.major}.{current_version.minor}.{current_version.micro}")
    print(f"   Required: {required_version[0]}.{required_version[1]}+")
    
    if current_version >= required_version:
        print("   ✅ Python version OK")
        return True
    else:
        print(f"   ❌ Python {required_version[0]}.{required_version[1]}+ required")
        print(f"   Download from: https://python.org")
        return False

def check_pip():
    """Check if pip is available"""
    print("Checking pip availability...")
    
    try:
        import pip
        print("   ✅ pip is available")
        return True
    except ImportError:
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            print("   ✅ pip is available via module")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ❌ pip not found")
            print("   Install pip: https://pip.pypa.io/en/stable/installation/")
            return False

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing dependencies...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("   ❌ requirements.txt not found")
        return False
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True, capture_output=True, text=True)
        
        print("   ✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print("   ❌ Failed to install dependencies")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error details: {e.stderr}")
        
        # Suggest common solutions
        print("\nCommon solutions:")
        print("   • Try: pip install --upgrade pip")
        print("   • Try: pip install --user -r requirements.txt")
        print("   • Check internet connection")
        print("   • Use virtual environment: python -m venv venv")
        
        return False
    
    except Exception as e:
        print(f"   ❌ Unexpected error during installation: {e}")
        return False

def check_imports():
    """Verify that required modules can be imported"""
    print("Verifying installed packages...")
    
    required_modules = [
        ("pydantic", "Pydantic for data validation"),
        ("urllib3", "HTTP client library"),
        ("dateutil", "Date utilities"),
        ("openapi_client", "Generated OpenAPI client")
    ]
    
    failed_imports = []
    
    for module_name, description in required_modules:
        try:
            if module_name == "openapi_client":
                # Check the local openapi_client
                spec = importlib.util.spec_from_file_location(
                    "openapi_client", 
                    Path(__file__).parent / "openapi_client" / "__init__.py"
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                else:
                    raise ImportError(f"Cannot load {module_name}")
            else:
                __import__(module_name)
            
            print(f"   ✅ {module_name}: OK")
            
        except ImportError as e:
            print(f"   ❌ {module_name}: Failed - {e}")
            failed_imports.append((module_name, description, str(e)))
        except Exception as e:
            print(f"   ⚠️  {module_name}: Warning - {e}")
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} import(s) failed:")
        for module, desc, error in failed_imports:
            print(f"   • {module} ({desc}): {error}")
        return False
    
    print("   ✅ All imports successful")
    return True

def setup_env_file():
    """Create .env file if it doesn't exist"""
    sdk_dir = Path(__file__).parent
    env_file = sdk_dir / ".env"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    # Create default .env
    print("Creating .env with default settings...")
    try:
        content = """# Maybind Python SDK Configuration
MAYBIND_API_KEY=your_api_key_here
MAYBIND_API_HOST=https://sdk.maybind.com
"""
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ .env created")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_api_key():
    """Get API key from .env file"""
    sdk_dir = Path(__file__).parent
    env_file = sdk_dir / ".env"
    
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip().startswith('MAYBIND_API_KEY='):
                        key = line.split('=', 1)[1].strip()
                        if key and key != "your_api_key_here":
                            return key
        except Exception:
            pass
    
    return None

def update_env_api_key(api_key):
    """Update the API key in .env file"""
    sdk_dir = Path(__file__).parent
    env_file = sdk_dir / ".env"
    
    try:
        # Read current content
        lines = []
        if env_file.exists():
            with open(env_file, 'r') as f:
                lines = f.readlines()
        
        # Update or add API key line
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith('MAYBIND_API_KEY='):
                lines[i] = f"MAYBIND_API_KEY={api_key}\n"
                updated = True
                break
        
        if not updated:
            # Add API key if not found
            lines.insert(1, f"MAYBIND_API_KEY={api_key}\n")
        
        # Write updated content
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        return True
    except Exception:
        return False

def verify_api_key(api_key):
    """Verify API key and get usage information"""
    try:
        from openapi_client.api.default_api import DefaultApi
        from openapi_client.configuration import Configuration
        from openapi_client.api_client import ApiClient
        from openapi_client.rest import ApiException
        
        print("Verifying API key with server...")
        
        # Configure client
        configuration = Configuration()
        configuration.host = os.getenv("MAYBIND_API_HOST", "https://sdk.maybind.com")
        configuration.api_key['ApiKeyAuth'] = api_key
        
        api_client = ApiClient(configuration)
        api = DefaultApi(api_client)
        
        # Call verify endpoint
        response = api.verify_api_key_verify_api_key_get()
        
        # Handle response
        if hasattr(response, 'to_dict'):
            response_data = response.to_dict()
        elif isinstance(response, dict):
            response_data = response
        else:
            response_data = {}
        
        print("✅ API key verification successful!")
        
        # Display key information
        key_name = response_data.get('key_name', 'Unknown')
        usage_count = response_data.get('usage_count', 'Unknown')
        
        print(f"   Key name: {key_name}")
        print(f"   Usage count: {usage_count}")
        
        if 'timestamp' in response_data:
            print(f"   Verified at: {response_data['timestamp']}")
        
        return True
        
    except ApiException as e:
        if e.status == 401:
            print("❌ API key verification failed - Invalid API key")
        elif e.status == 404:
            print("⚠️  Verify endpoint not available (404)")
        else:
            print(f"❌ API error: {e.status} - {e.reason}")
        return False
        
    except ImportError as e:
        print(f"⚠️  Cannot verify - Import error: {e}")
        print("   This might be normal if dependencies are not yet installed")
        return None
        
    except Exception as e:
        print(f"❌ Verification error: {type(e).__name__}: {e}")
        return False

def test_unauthenticated_api():
    """Test unauthenticated endpoints to verify API connectivity"""
    print("Testing API connectivity (without authentication)...")
    
    try:
        from openapi_client.api.default_api import DefaultApi
        from openapi_client.configuration import Configuration
        from openapi_client.api_client import ApiClient
        from openapi_client.rest import ApiException
        
        # Configure client without API key
        configuration = Configuration()
        configuration.host = os.getenv("MAYBIND_API_HOST", "https://sdk.maybind.com")
        
        api_client = ApiClient(configuration)
        api = DefaultApi(api_client)
        
        # Test health endpoint (should work without auth)
        response = api.health_check_health_get()
        return True
        
    except ApiException as e:
        if e.status == 401:
            return True  # Server is reachable, just requires auth
        else:
            print(f"   ❌ API connectivity test failed: {e.status} - {e.reason}")
            return False
            
    except Exception as e:
        print(f"   ❌ API connectivity test failed: {type(e).__name__}: {e}")
        return False

def prompt_for_valid_api_key():
    """Prompt user for a valid API key with detailed instructions"""
    print("\nAPI Key Setup Required")
    print("=" * 40)
    print("To use the Maybind SDK, you need a valid API key.")
    print("\nHow to get your API key:")
    print("   1. Visit: https://maybind.com")
    print("   2. Click 'Login' and sign in to your account")
    print("   3. Go to your dashboard/settings")
    print("   4. Click 'Generate Token' or 'API Keys'")
    print("   5. Copy the generated API key")
    print("\nIf you don't have an account:")
    print("   • Sign up at https://maybind.com")
    print("   • Complete account verification")
    print("   • Generate your first API key")
    
    while True:
        print("\n" + "="*50)
        try:
            choice = input("Do you want to enter your API key now? (y/n): ").lower().strip()
            
            if choice in ['y', 'yes']:
                api_key = getpass.getpass("\nEnter your API key (hidden): ").strip()
                if not api_key:
                    print("❌ No API key provided. Please try again.")
                    continue
                
                # Update .env file
                if update_env_api_key(api_key):
                    print("✅ API key saved to .env file")
                    
                    # Test the new API key
                    print("\nTesting your API key...")
                    if verify_api_key(api_key):
                        print("🎉 Perfect! Your API key is valid and working.")
                        return True
                    else:
                        print("❌ The API key you entered is not valid.")
                        print("Please check that you copied it correctly.")
                        continue
                else:
                    print("❌ Failed to save API key to .env file")
                    return False
                    
            elif choice in ['n', 'no']:
                print("\n⚠️  Setup completed without API key verification.")
                print("You can add your API key later by:")
                print("   • Editing the .env file manually")
                print("   • Running this setup script again")
                return False
                
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                
        except KeyboardInterrupt:
            print("\n❌ Setup cancelled by user")
            return False
        except Exception as e:
            print(f"❌ Error during API key input: {e}")
            return False

def main():
    """Quick setup with prerequisite checks and dependency installation"""
    print_header()
    
    # Step 1: Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python version requirement not met")
        sys.exit(1)
    
    # Step 2: Check pip
    if not check_pip():
        print("\n❌ Setup failed: pip not available")
        sys.exit(1)
    
    # Step 3: Install requirements
    if not install_requirements():
        print("\n❌ Setup failed: Could not install dependencies")
        print("� Try running manually: pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 4: Verify imports
    if not check_imports():
        print("\n❌ Setup failed: Import verification failed")
        print("💡 Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 5: Setup .env file
    if not setup_env_file():
        print("\n❌ Setup failed: Could not create .env file")
        sys.exit(1)
    
    # Step 6: Check API key
    api_key = get_api_key()
    if not api_key:
        print("⚠️  No valid API key found")
        print("� Please enter your Maybind API key:")
        
        # Interactive API key input
        try:
            api_key = getpass.getpass("API Key (hidden): ").strip()
            if not api_key:
                print("❌ No API key provided")
                return
            
            # Update .env file with the new API key
            update_env_api_key(api_key)
            print("✅ API key saved to .env file")
            
        except KeyboardInterrupt:
            print("\n❌ Setup cancelled")
            return
        except Exception as e:
            print(f"❌ Error reading API key: {e}")
            return
    
    print(f"API key found: {api_key[:8]}...")
    
    # Step 7: Verify API key
    verification_result = verify_api_key(api_key)
    
    if verification_result is True:
        print("\n🎉 Setup complete! API key is valid and ready to use.")
    elif verification_result is False:
        print("\n⚠️  API key verification failed.")
        
        # Test unauthenticated API to check connectivity
        if test_unauthenticated_api():
            # Prompt for a valid API key
            if prompt_for_valid_api_key():
                print("\n🎉 Setup complete! API key is now valid and ready to use.")
        else:
            print("❌ Cannot reach API server. Please check:")
            print("   • Internet connection")
            print("   • API host URL in .env file")
            print("   • Firewall settings")
        return
    else:  # verification_result is None
        print("\n⚠️  Setup complete, but API key verification was skipped.")
        print("You may need to install dependencies manually if verification fails.")
    
    # Step 8: Next steps
    print("\nNext steps:")
    print("   • Run tests: python -m pytest tests/ -v")
    print("   • Check examples: examples/")
    print("   • Read documentation in README.md")
    print("   • Visit https://maybind.com for more information")

if __name__ == "__main__":
    main()
