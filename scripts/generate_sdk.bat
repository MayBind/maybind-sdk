@echo off
REM Script to generate SDK from OpenAPI specification (Windows batch version)
REM This script regenerates both Python and JavaScript SDKs from the OpenAPI spec

echo Maybind SDK Generator
echo ====================

REM Configuration
set OPENAPI_SPEC=./openapi/maybind-api.yaml
set PYTHON_OUTPUT_DIR=./sdk/python
set JAVASCRIPT_OUTPUT_DIR=./sdk/javascript
set GENERATOR_VERSION=v7.0.1

REM Check if OpenAPI spec exists
if not exist "%OPENAPI_SPEC%" (
    echo [ERROR] OpenAPI specification not found at %OPENAPI_SPEC%
    exit /b 1
)

echo [INFO] Found OpenAPI specification at %OPENAPI_SPEC%

REM Check if OpenAPI Generator is installed
openapi-generator version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] OpenAPI Generator not found. Please install it manually.
    echo [INFO] See: https://openapi-generator.tech/docs/installation
    echo [INFO] Or install via npm: npm install -g @openapitools/openapi-generator-cli
    exit /b 1
)

echo [INFO] OpenAPI Generator is available

REM Generate Python SDK
echo [INFO] Generating Python SDK...
openapi-generator generate ^
    -i "%OPENAPI_SPEC%" ^
    -g python ^
    -o "%PYTHON_OUTPUT_DIR%" ^
    --package-name openapi_client ^
    --additional-properties=packageName=openapi_client,projectName=maybind-sdk,packageVersion=1.0.0

if %errorlevel% neq 0 (
    echo [ERROR] Python SDK generation failed
    exit /b 1
)

echo [INFO] Python SDK generated successfully

REM Generate JavaScript SDK
echo [INFO] Generating JavaScript SDK...
openapi-generator generate ^
    -i "%OPENAPI_SPEC%" ^
    -g javascript ^
    -o "%JAVASCRIPT_OUTPUT_DIR%" ^
    --additional-properties=projectName=maybind-sdk,projectVersion=1.0.0,moduleName=MaybindSDK

if %errorlevel% neq 0 (
    echo [ERROR] JavaScript SDK generation failed
    exit /b 1
)

echo [INFO] JavaScript SDK generated successfully

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
if exist "%PYTHON_OUTPUT_DIR%\requirements.txt" (
    cd "%PYTHON_OUTPUT_DIR%"
    pip install -r requirements.txt
    cd ..\..\
)

REM Install JavaScript dependencies
echo [INFO] Installing JavaScript dependencies...
if exist "%JAVASCRIPT_OUTPUT_DIR%\package.json" (
    cd "%JAVASCRIPT_OUTPUT_DIR%"
    npm install
    cd ..\..\
)

echo [INFO] SDK generation completed successfully!
echo [INFO] Python SDK: %PYTHON_OUTPUT_DIR%
echo [INFO] JavaScript SDK: %JAVASCRIPT_OUTPUT_DIR%

echo.
echo Next steps:
echo 1. Test the generated SDKs with the examples in ./sdk/python/examples/
echo 2. Run tests with: cd sdk/python ^&^& python -m pytest tests/
echo 3. Update documentation if needed

pause
