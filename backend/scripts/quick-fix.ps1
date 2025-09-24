# Quick fix script for RepoScope backend
# This script runs all code quality fixes automatically

Write-Host "🚀 Running RepoScope code quality fixes..." -ForegroundColor Green
Write-Host ""

# Change to backend directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath ".."
Set-Location $backendPath

# Run the fix script
python scripts/fix-code-quality.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ All fixes completed successfully!" -ForegroundColor Green
    Write-Host "💡 You can now commit your changes safely." -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Some fixes failed. Please check the output above." -ForegroundColor Red
    Write-Host "💡 Fix the issues manually and run this script again." -ForegroundColor Yellow
}

Read-Host "Press Enter to continue"
