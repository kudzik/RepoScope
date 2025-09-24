@echo off
echo Auto-fixing and committing changes...

cd backend

REM Fix formatting and imports
python -m black .
python -m isort . --force-single-line-imports

REM Check if everything is OK
python -m flake8 . --extend-ignore=E203,C901,D401,I100,I101,I201,I202
if %errorlevel% neq 0 (
    echo Flake8 errors found, please fix manually
    exit /b 1
)

echo All checks passed, committing...
cd ..
git add .
git commit -m "feat(backend): rozszerzenie CodeAnalyzer o zaawansowane metryki Tree-sitter"

echo Commit completed successfully!
