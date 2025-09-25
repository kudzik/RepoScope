@echo off
echo Fixing pre-commit issues automatically...

REM Run auto-fix script
python scripts/auto-commit-fix.py

REM Run formatters
python -m black .
python -m isort .

REM Try commit
git add .
git commit -m "feat: auto-fixed pre-commit issues"

echo Done!
