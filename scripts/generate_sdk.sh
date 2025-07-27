#!/bin/bash
# Script to generate SDK from OpenAPI specification
# This script regenerates both Python and JavaScript SDKs from the OpenAPI spec

set -e

echo "Maybind SDK Generator"
echo "===================="

# Configuration
OPENAPI_SPEC="./openapi/maybind-api.yaml"
PYTHON_OUTPUT_DIR="./sdk/python"
JAVASCRIPT_OUTPUT_DIR="./sdk/javascript"
GENERATOR_VERSION="v7.0.1"  # OpenAPI Generator version

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if OpenAPI spec exists
if [ ! -f "$OPENAPI_SPEC" ]; then
    print_error "OpenAPI specification not found at $OPENAPI_SPEC"
    exit 1
fi

print_status "Found OpenAPI specification at $OPENAPI_SPEC"

# Check if OpenAPI Generator is installed
if ! command -v openapi-generator &> /dev/null; then
    print_warning "OpenAPI Generator not found. Installing..."
    
    # Install OpenAPI Generator (requires Java)
    if command -v npm &> /dev/null; then
        npm install -g @openapitools/openapi-generator-cli
    elif command -v brew &> /dev/null; then
        brew install openapi-generator
    else
        print_error "Please install OpenAPI Generator manually"
        print_error "See: https://openapi-generator.tech/docs/installation"
        exit 1
    fi
fi

print_status "OpenAPI Generator is available"

# Generate Python SDK
print_status "Generating Python SDK..."
openapi-generator generate \
    -i "$OPENAPI_SPEC" \
    -g python \
    -o "$PYTHON_OUTPUT_DIR" \
    --package-name openapi_client \
    --additional-properties=packageName=openapi_client,projectName=maybind-sdk,packageVersion=1.0.0

print_status "Python SDK generated successfully"

# Generate JavaScript SDK
print_status "Generating JavaScript SDK..."
openapi-generator generate \
    -i "$OPENAPI_SPEC" \
    -g javascript \
    -o "$JAVASCRIPT_OUTPUT_DIR" \
    --additional-properties=projectName=maybind-sdk,projectVersion=1.0.0,moduleName=MaybindSDK

print_status "JavaScript SDK generated successfully"

# Install Python dependencies
print_status "Installing Python dependencies..."
if [ -f "$PYTHON_OUTPUT_DIR/requirements.txt" ]; then
    cd "$PYTHON_OUTPUT_DIR"
    pip install -r requirements.txt
    cd - > /dev/null
fi

# Install JavaScript dependencies
print_status "Installing JavaScript dependencies..."
if [ -f "$JAVASCRIPT_OUTPUT_DIR/package.json" ]; then
    cd "$JAVASCRIPT_OUTPUT_DIR"
    npm install
    cd - > /dev/null
fi

print_status "SDK generation completed successfully!"
print_status "Python SDK: $PYTHON_OUTPUT_DIR"
print_status "JavaScript SDK: $JAVASCRIPT_OUTPUT_DIR"

echo ""
echo "Next steps:"
echo "1. Test the generated SDKs with the examples in ./sdk/python/examples/"
echo "2. Run tests with: cd sdk/python && python -m pytest tests/"
echo "3. Update documentation if needed"
