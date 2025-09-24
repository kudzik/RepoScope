@echo off
REM Quick fix script for RepoScope backend
REM This script runs all code quality fixes automatically

echo 🚀 Running RepoScope code quality fixes...
echo.

cd /d "%~dp0.."
python scripts/fix-code-quality.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ All fixes completed successfully!
    echo 💡 You can now commit your changes safely.
) else (
    echo.
    echo ❌ Some fixes failed. Please check the output above.
    echo 💡 Fix the issues manually and run this script again.
)

pause
