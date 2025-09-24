#!/bin/bash
# Pre-commit fix script to automatically resolve common issues

echo "🔧 Running pre-commit fixes..."

# 1. Fix imports with isort
echo "📦 Sorting imports with isort..."
python -m isort main.py api/ schemas/ services/ tests/ --profile black --line-length=100

# 2. Format code with black
echo "🎨 Formatting code with black..."
python -m black main.py api/ schemas/ services/ tests/ --line-length=100

# 3. Fix end of files
echo "📄 Fixing end of files..."
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
echo "📋 Fixing requirements.txt..."
if [ -f "requirements.txt" ]; then
    python -c "
import re
with open('requirements.txt', 'r') as f:
    lines = f.readlines()
# Sort lines alphabetically
lines.sort()
with open('requirements.txt', 'w') as f:
    f.writelines(lines)
"
fi

echo "✅ Pre-commit fixes completed!"
