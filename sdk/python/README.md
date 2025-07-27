# Maybind Python SDK

Professional Python SDK for interacting with Maybind's AI Twin platform. This SDK provides easy-to-use interfaces for twin management, chat functionality, and API key verification.

## 🚀 Quick Start

### Installation

```bash
# Quick setup with automatic configuration
python setup_quick.py

# Or manual installation
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the SDK directory:

```bash
# Maybind Python SDK Configuration
MAYBIND_API_KEY=your_api_key_here
MAYBIND_API_HOST=https://sdk.maybind.com
MAYBIND_TWIN_ID=01
```

## � Usage Examples

### Quick Example

```python
from openapi_client import ApiClient, Configuration
from openapi_client.api.default_api import DefaultApi
from openapi_client.models.chat_request import ChatRequest

# Quick setup
config = Configuration()
config.host = "https://sdk.maybind.com"
config.api_key['ApiKeyAuth'] = "your_api_key_here"

api = DefaultApi(ApiClient(config))

# Get available twins
twins = api.get_users_users_get()
twin_id = twins.to_dict()['twin_ids'][0]

# Chat with twin
chat_request = ChatRequest(
    twin_id=twin_id,
    messages=[{
        "timestamp": "2025-07-17T16:00:00Z",
        "text": "Hello!",
        "role": "user"
    }]
)

response = api.chat_chat_post(chat_request)
print(f"Twin: {response.to_dict()['messages'][-1]['text']}")
```

### Complete Interactive Example

```python
#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add SDK to path
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
    """Get list of available twins from the users API"""
    try:
        response = api_instance.get_users_users_get()
        users_data = response.to_dict() if hasattr(response, 'to_dict') else response
        
        if isinstance(users_data, dict) and 'twin_ids' in users_data:
            return users_data['twin_ids'][0] if users_data['twin_ids'] else None
        return None
    except Exception:
        return None

def main():
    # Load configuration
    env_config = load_env_config()
    
    # Setup API client
    configuration = Configuration()
    configuration.host = env_config.get("MAYBIND_API_HOST", "https://sdk.maybind.com")
    configuration.api_key['ApiKeyAuth'] = env_config.get("MAYBIND_API_KEY")
    
    api_client = ApiClient(configuration)
    api_instance = DefaultApi(api_client)
    
    # Get available twins
    twin_id = get_available_twins(api_instance) or "twin_001"
    
    # Create chat request
    chat_request = ChatRequest(
        twin_id=twin_id,
        messages=[{
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "text": "Hello, how are you?",
            "role": "user"
        }]
    )
    
    # Send chat message
    response = api_instance.chat_chat_post(chat_request)
    response_data = response.to_dict() if hasattr(response, 'to_dict') else response
    
    # Display conversation
    print(f"Conversation with {response_data.get('twin_id')}:")
    for msg in response_data.get('messages', []):
        role_icon = "👤" if msg.get('role') == 'user' else "🤖"
        print(f"  {role_icon} {msg.get('role')}: {msg.get('text')}")

if __name__ == "__main__":
    main()
```

**Note:** Authentication and API key verification is handled by `setup_quick.py`

## 🛠️ Available Scripts

- **`setup_quick.py`** - Quick setup with API key verification and usage stats
- **`examples/example_chat.py`** - Complete chat example with twin selection

## 📚 API Reference

### Configuration

```python
from openapi_client import Configuration

configuration = Configuration()
configuration.host = "https://sdk.maybind.com"
configuration.api_key['ApiKeyAuth'] = 'your_api_key_here'
```

### Chat Request Format

```python
from openapi_client.models.chat_request import ChatRequest
from datetime import datetime, timezone

chat_request = ChatRequest(
    twin_id="twin_001",
    messages=[{
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "text": "Your message here",
        "role": "user"
    }]
)
```

## 🔧 Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send chat messages to twins |
| `GET` | `/users` | Get available twins |
| `GET` | `/verify-api-key` | Verify API key validity |
| `GET` | `/health` | Health check |

## 🔐 Authentication

The SDK uses API key authentication via the `X-Api-Key` header:

```python
configuration.api_key['ApiKeyAuth'] = 'your_api_key_here'
```

## 📄 License

This SDK is part of the Maybind platform.

---

For more examples and detailed documentation, check the `examples/` directory.




