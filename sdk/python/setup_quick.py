#!/usr/bin/env python3
"""
Quick setup for MayBind Python SDK
"""

import os
from pathlib import Path

def setup_env_file():
    """Create .env file if it doesn't exist"""
    sdk_dir = Path(__file__).parent
    env_file = sdk_dir / ".env"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    # Create default .env
    print("📝 Creating .env with default settings...")
    try:
        content = """# MayBind Python SDK Configuration
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
        
        print("🔐 Verifying API key with server...")
        
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
        
        print(f"🏷️  Key name: {key_name}")
        print(f"📊 Usage count: {usage_count}")
        
        if 'timestamp' in response_data:
            print(f"⏰ Verified at: {response_data['timestamp']}")
        
        return True
        
    except ApiException as e:
        if e.status == 401:
            print("❌ API key verification failed - Invalid API key")
        elif e.status == 404:
            print("⚠️  Verify endpoint not available (404)")
        else:
            print(f"❌ API error: {e.status} - {e.reason}")
        return False
        
    except ImportError:
        print("⚠️  Cannot verify - SDK not installed")
        print("   Run: pip install -e .")
        return None
        
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def main():
    """Quick setup with API key verification"""
    print("🚀 MayBind SDK Quick Setup")
    print("=" * 30)
    
    # 1. Setup .env file
    if not setup_env_file():
        return
    
    # 2. Check API key
    api_key = get_api_key()
    if not api_key:
        print("⚠️  No valid API key found")
        print("� Please enter your MayBind API key:")
        
        # Interactive API key input
        try:
            api_key = input("API Key: ").strip()
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
    
    print(f"🔑 API key found: {api_key[:8]}...")
    
    # 3. Verify API key
    verification_result = verify_api_key(api_key)
    
    if verification_result is True:
        print("\n✅ Setup complete! API key is valid and ready to use.")
    elif verification_result is False:
        print("\n❌ Setup incomplete - API key verification failed.")
        print("📝 Please check your API key in .env file")
        return
    else:  # verification_result is None
        print("\n⚠️  Setup complete, but API key verification was skipped.")
    
    # 4. Next steps
    print("\nNext steps:")
    print("• Run tests: python -m pytest tests/ -v")
    print("• Check examples: examples/")

if __name__ == "__main__":
    main()
