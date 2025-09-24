# Pre-commit fix script to automatically resolve common issues

Write-Host "🔧 Running pre-commit fixes..." -ForegroundColor Green

# 1. Fix imports with isort
Write-Host "📦 Sorting imports with isort..." -ForegroundColor Yellow
python -m isort main.py api/ schemas/ services/ tests/ --profile black --line-length=100

# 2. Format code with black
Write-Host "🎨 Formatting code with black..." -ForegroundColor Yellow
python -m black main.py api/ schemas/ services/ tests/ --line-length=100

# 3. Fix end of files
Write-Host "📄 Fixing end of files..." -ForegroundColor Yellow
python -c "
import os
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'rb') as f:
                content = f.read()
            if content and not content.endswith(b'\n'):
                with open(filepath, 'wb') as f:
                    f.write(content + b'\n')
"

# 4. Fix requirements.txt
Write-Host "📋 Fixing requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    python -c "
import re
with open('requirements.txt', 'r') as f:
    lines = f.readlines()
# Sort lines alphabetically
lines.sort()
with open('requirements.txt', 'w') as f:
    f.writelines(lines)
"
}

Write-Host "✅ Pre-commit fixes completed!" -ForegroundColor Green
