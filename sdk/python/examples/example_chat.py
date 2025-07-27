#!/usr/bin/env python3
"""
Example usage of Maybind SDK for chat functionality.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from openapi_client import ApiClient, Configuration
from openapi_client.api.default_api import DefaultApi
from openapi_client.models.chat_request import ChatRequest


def load_env_config():
    """Load configuration from .env file"""
    sdk_dir = Path(__file__).parent.parent
    env_file = sdk_dir / ".env"
    
    config = {}
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key] = value
        except Exception:
            pass
    
    return config


def get_available_twins(api_instance):
    """
    Get list of available twins from the users API.
    Returns the first available twin ID or None if no twins found.
    """
    try:
        print("📋 Fetching available twins...")
        response = api_instance.get_users_users_get()
        
        if hasattr(response, 'to_dict'):
            users_data = response.to_dict()
        else:
            users_data = response
        
        print(f"✓ Users API response received")
        # print(f"📊 Response data: {users_data}")  # Debug output removed
        
        # Extract twin IDs from the response
        twin_ids = []
        if isinstance(users_data, dict) and 'twin_ids' in users_data:
            twin_ids = users_data['twin_ids']
        elif isinstance(users_data, list):
            for user in users_data:
                if isinstance(user, dict) and 'twin_id' in user:
                    twin_ids.append(user['twin_id'])
                elif isinstance(user, dict) and 'id' in user:
                    twin_ids.append(user['id'])
        elif isinstance(users_data, dict):
            # Handle other response structures
            if 'twins' in users_data:
                twin_ids = users_data['twins']
            elif 'users' in users_data:
                for user in users_data['users']:
                    if 'twin_id' in user:
                        twin_ids.append(user['twin_id'])
                    elif 'id' in user:
                        twin_ids.append(user['id'])
        
        if twin_ids:
            print(f"✓ Found {len(twin_ids)} available twins: {twin_ids}")
            return twin_ids[0]  # Return first available twin
        else:
            print("⚠️  No twins found in response, using fallback")
            return None
            
    except Exception as e:
        print(f"⚠️  Error fetching twins: {e}")
        print("   Using fallback twin ID")
        return None


def main():
    """
    Example demonstrating how to use the Maybind SDK for chat.
    """
    
    # Load from .env file first, then environment variables
    env_config = load_env_config()
    
    # Configuration
    configuration = Configuration()
    configuration.host = env_config.get("MAYBIND_API_HOST") or os.getenv("MAYBIND_API_HOST", "https://sdk.maybind.com")
    
    # Configure API key from .env or environment
    api_key = env_config.get("MAYBIND_API_KEY") or os.getenv("MAYBIND_API_KEY")
    
    if api_key and api_key != "your_api_key_here":
        configuration.api_key['ApiKeyAuth'] = api_key
        print(f"✓ API key loaded from configuration")
    else:
        print("⚠️  No valid API key found")
        print("   Make sure MAYBIND_API_KEY is set in .env file")
        print("   Continuing with mock example...")
    
    # Create API client
    api_client = ApiClient(configuration)
    api_instance = DefaultApi(api_client)
    
    # Get available twins from API or use fallback
    if api_key and api_key != "your_api_key_here":
        twin_id = get_available_twins(api_instance)
        if not twin_id:
            # Fallback to configured twin ID
            twin_id = env_config.get("MAYBIND_TWIN_ID") or os.getenv("MAYBIND_TWIN_ID", "01")
            print(f"📌 Using fallback twin ID: {twin_id}")
    else:
        # No API key, use configured twin ID
        twin_id = env_config.get("MAYBIND_TWIN_ID") or os.getenv("MAYBIND_TWIN_ID", "01")
        print(f"📌 Using configured twin ID: {twin_id}")
    
    # Create a chat request with proper message format
    current_time = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    chat_request = ChatRequest(
        twin_id=twin_id,
        messages=[
            {
                "timestamp": current_time,
                "text": "Hello, how are you?",
                "role": "user"
            }
        ]
    )
    
    print(f"\nConfiguration:")
    print(f"  Host: {configuration.host}")
    print(f"  Twin ID: {chat_request.twin_id}")
    print(f"  Messages: {len(chat_request.messages)}")
    
    try:
        # Make API call only if we have a valid API key
        if api_key and api_key != "your_api_key_here":
            print("\nMaking real API call...")
            response = api_instance.chat_chat_post(chat_request)
            
            if hasattr(response, 'to_dict'):
                response_data = response.to_dict()
            else:
                response_data = response
            
            print(f"✓ Chat completed successfully!")
            print(f"📞 Conversation with {response_data.get('twin_id', twin_id)}:")
            
            messages = response_data.get('messages', [])
            for msg in messages:
                role_icon = "👤" if msg.get('role') == 'user' else "🤖"
                print(f"  {role_icon} {msg.get('role', 'unknown')}: {msg.get('text', '')}")
                
        else:
            print("\nSimulating API call...")
            print(f"✓ Request prepared successfully")
            print(f"  Request data: {chat_request.to_dict()}")
            
    except Exception as e:
        print(f"✗ Error during API call: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
