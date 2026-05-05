#!/bin/bash
# Setup script for GitHub Pages deployment
# Run this to prepare your project for GitHub Pages

set -e  # Exit on error

echo "🚀 SENTINEL GitHub Pages Setup"
echo "================================"

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found"

# Create directories
echo "📁 Creating deployment directories..."
mkdir -p .github/workflows
mkdir -p gh-pages
mkdir -p js

# Install dependencies if needed
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Export model
if [ -f "export_model.py" ]; then
    echo "🤖 Exporting model weights..."
    python export_model.py
    echo "✅ Model exported"
else
    echo "⚠️  export_model.py not found"
fi

# Copy files to gh-pages
echo "📋 Copying files to gh-pages directory..."
cp index-gh-pages.html gh-pages/index.html 2>/dev/null || echo "⚠️  index-gh-pages.html not found"
cp model_weights.json gh-pages/ 2>/dev/null || echo "⚠️  model_weights.json not found"
cp -r js/*.js gh-pages/js/ 2>/dev/null || echo "⚠️  js files not found"

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review your deployment in gh-pages/ directory"
echo "2. Test locally: python app.py"
echo "3. Push to GitHub: git push origin main"
echo "4. Enable GitHub Pages in repository Settings"
echo "5. Visit: https://YOUR-USERNAME.github.io/YOUR-REPO/"
echo ""
echo "📖 See GITHUB_PAGES_DEPLOYMENT.md for detailed instructions"
