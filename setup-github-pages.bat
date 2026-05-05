@echo off
REM Setup script for GitHub Pages deployment (Windows version)
REM Run this to prepare your project for GitHub Pages

echo.
echo 🚀 SENTINEL GitHub Pages Setup
echo ================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

echo ✅ Python found

REM Create directories
echo 📁 Creating deployment directories...
if not exist ".github\workflows" mkdir .github\workflows
if not exist "gh-pages" mkdir gh-pages
if not exist "js" mkdir js

REM Install dependencies
if exist "requirements.txt" (
    echo 📦 Installing Python dependencies...
    python -m pip install -r requirements.txt
)

REM Export model
if exist "export_model.py" (
    echo 🤖 Exporting model weights...
    python export_model.py
    echo ✅ Model exported
) else (
    echo ⚠️  export_model.py not found
)

REM Copy files to gh-pages
echo 📋 Copying files to gh-pages directory...
if exist "index-gh-pages.html" (
    copy index-gh-pages.html gh-pages\index.html >nul
) else (
    echo ⚠️  index-gh-pages.html not found
)

if exist "model_weights.json" (
    copy model_weights.json gh-pages\ >nul
) else (
    echo ⚠️  model_weights.json not found
)

if exist "js" (
    xcopy js\*.js gh-pages\js\ /Y >nul
) else (
    echo ⚠️  js files not found
)

echo.
echo ✨ Setup complete!
echo.
echo Next steps:
echo 1. Review your deployment in gh-pages\ directory
echo 2. Test locally: python app.py
echo 3. Push to GitHub: git push origin main
echo 4. Enable GitHub Pages in repository Settings
echo 5. Visit: https://YOUR-USERNAME.github.io/YOUR-REPO/
echo.
echo 📖 See GITHUB_PAGES_DEPLOYMENT.md for detailed instructions
echo.
pause
