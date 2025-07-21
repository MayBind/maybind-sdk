@echo off
REM Script to sync OpenAPI spec from root to docs folder
REM Run this after updating openapi/maybind-api.yaml

echo Syncing OpenAPI spec to docs folder...

if not exist "openapi\maybind-api.yaml" (
    echo [ERROR] Source file openapi\maybind-api.yaml not found
    exit /b 1
)

if not exist "docs\openapi" (
    mkdir "docs\openapi"
)

copy "openapi\maybind-api.yaml" "docs\openapi\maybind-api.yaml" >nul

if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] OpenAPI spec synced to docs/openapi/
) else (
    echo [ERROR] Failed to sync OpenAPI spec
    exit /b 1
)
