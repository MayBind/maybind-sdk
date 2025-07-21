# MayBind SDK Tests

This directory contains essential tests for the MayBind SDK that developers can run to verify their setup.

## Test Files

- `test_sdk_basic.py` - Core SDK functionality tests (no API calls required)
- `test_integration.py` - Integration tests with real API (requires API key)

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r test-requirements.txt
```

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Basic Tests Only (no API key needed)
```bash
python -m pytest tests/test_sdk_basic.py -v
```

### Run Integration Tests (API key required)
```bash
# Set your API key first
export MAYBIND_API_KEY="your_api_key_here"
python -m pytest tests/test_integration.py -v
```

### Run with Coverage
```bash
python -m pytest tests/ --cov=openapi_client --cov-report=html
```

## Test Overview

### Basic Tests (`test_sdk_basic.py`)
- ✅ Configuration creation and setup
- ✅ API client initialization  
- ✅ Request object creation
- ✅ Complete SDK setup workflow
- ✅ Environment variable configuration

These tests verify that the SDK is properly installed and can be used without making actual API calls.

### Integration Tests (`test_integration.py`)
- 🔑 API key verification (requires valid API key)
- 🔑 Complete developer workflow testing

These tests require a valid `MAYBIND_API_KEY` environment variable and test actual API interactions.

## For Developers

The tests are designed to be simple and practical, focusing on the most common SDK usage patterns:

1. **Start with basic tests** to verify SDK installation
2. **Add your API key** to environment variables  
3. **Run integration tests** to verify API connectivity
4. **Use the test patterns** as examples for your own code
