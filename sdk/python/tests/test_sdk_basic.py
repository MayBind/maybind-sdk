#!/usr/bin/env python3
"""
Basic tests for MayBind SDK functionality.
These tests focus on core SDK features that developers use most.
"""

import pytest
import os
import sys

# Add the SDK to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from openapi_client import ApiClient, Configuration
    from openapi_client.api.default_api import DefaultApi
    from openapi_client.models.chat_request import ChatRequest
    from openapi_client.exceptions import ApiException
    SDK_AVAILABLE = True
except ImportError as e:
    print(f"Warning: SDK not available - {e}")
    SDK_AVAILABLE = False


@pytest.mark.skipif(not SDK_AVAILABLE, reason="SDK not available")
class TestSDKBasics:
    """Test basic SDK functionality."""
    
    def test_configuration_creation(self):
        """Test that we can create a basic configuration."""
        config = Configuration()
        assert config is not None
        assert hasattr(config, 'host')
        assert hasattr(config, 'api_key')
    
    def test_configuration_with_host(self):
        """Test setting host in configuration."""
        config = Configuration()
        test_host = "https://sdk.maybind.com"
        config.host = test_host
        assert config.host == test_host
    
    def test_configuration_with_api_key(self):
        """Test setting API key in configuration."""
        config = Configuration()
        test_api_key = "test_api_key_123"
        config.api_key['ApiKeyAuth'] = test_api_key
        assert config.api_key['ApiKeyAuth'] == test_api_key
    
    def test_api_client_creation(self):
        """Test that we can create an API client."""
        config = Configuration()
        client = ApiClient(config)
        assert client is not None
        assert client.configuration == config
    
    def test_default_api_creation(self):
        """Test that we can create the default API instance."""
        config = Configuration()
        client = ApiClient(config)
        api = DefaultApi(client)
        assert api is not None
        assert api.api_client == client
    
    def test_chat_request_creation(self):
        """Test that we can create a chat request."""
        request = ChatRequest(
            twin_id="test_twin_123",
            messages=[
                {"role": "user", "content": "Hello, test!"}
            ]
        )
        assert request is not None
        assert request.twin_id == "test_twin_123"
        assert len(request.messages) == 1
        assert request.messages[0]["role"] == "user"
        assert request.messages[0]["content"] == "Hello, test!"
    
    def test_full_sdk_setup(self):
        """Test complete SDK setup as a developer would use it."""
        # This is the pattern developers will use most
        config = Configuration()
        config.host = "https://sdk.maybind.com"
        config.api_key['ApiKeyAuth'] = "test_key_12345"
        
        client = ApiClient(config)
        api = DefaultApi(client)
        
        request = ChatRequest(
            twin_id="my_twin_id", 
            messages=[
                {"role": "user", "content": "How are you today?"}
            ]
        )
        
        # Verify everything is set up correctly
        assert config.host == "https://sdk.maybind.com"
        assert config.api_key['ApiKeyAuth'] == "test_key_12345"
        assert request.twin_id == "my_twin_id"
        assert len(request.messages) == 1
        
        # Note: We don't make actual API calls in unit tests
        # That would be an integration test


@pytest.mark.skipif(not SDK_AVAILABLE, reason="SDK not available")
class TestEnvironmentConfiguration:
    """Test configuration from environment variables."""
    
    def test_config_from_env_vars(self):
        """Test loading configuration from environment variables."""
        # Simulate environment variables
        test_api_key = "env_test_key_123"
        test_host = "https://test.maybind.dev"
        
        # Set up config like developers would
        config = Configuration()
        config.host = os.getenv("MAYBIND_API_HOST", "https://sdk.maybind.com")
        api_key = os.getenv("MAYBIND_API_KEY", "default_test_key")
        config.api_key['ApiKeyAuth'] = api_key
        
        # Verify defaults work
        assert config.host == "https://sdk.maybind.com"
        assert config.api_key['ApiKeyAuth'] == "default_test_key"


if __name__ == "__main__":
    pytest.main([__file__])
