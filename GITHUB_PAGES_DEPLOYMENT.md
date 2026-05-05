# 🚀 SENTINEL - GitHub Pages Deployment Guide

This project now supports **two deployment modes**:

## 📋 Deployment Options

### Option 1: Local Development (Flask Backend)
Run the Flask server locally with full Python capabilities:
```bash
python app.py
```
Open `http://localhost:5000` in your browser.

### Option 2: GitHub Pages (Pure Frontend - Recommended)
Deploy as a static website on GitHub Pages with no backend required.

---

## 🌐 GitHub Pages Deployment

### Prerequisites
- GitHub account with a repository
- Git installed locally
- Python 3.8+ (for model export)

### Step-by-Step Setup

#### 1. **Prepare Your Repository**

Initialize git if not already done:
```bash
git init
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
```

#### 2. **Export Model Weights**

Generate pre-trained weights for the frontend:
```bash
python export_model.py
```

This creates `model_weights.json` containing all trained weights.

#### 3. **Manual Deployment (Without GitHub Actions)**

Copy files to a deployment directory:
```bash
# Create deployment folder
mkdir -p gh-pages

# Copy files
cp index-gh-pages.html gh-pages/index.html
cp model_weights.json gh-pages/
cp -r js gh-pages/
```

Push to GitHub:
```bash
git add .
git commit -m "Add GitHub Pages deployment files"
git push origin main
```

#### 4. **Enable GitHub Pages (Automatic with GitHub Actions)**

If you push the `.github/workflows/deploy.yml` file, GitHub Actions will automatically:
- Export model weights
- Build the deployment
- Deploy to GitHub Pages

**Manual setup (if GitHub Actions doesn't work):**

1. Go to your repository Settings
2. Scroll to "Pages" section
3. Set deployment source:
   - **Source**: GitHub Actions
   - OR manually select branch: `gh-pages` (if you created it)

4. Your site will be available at:
   ```
   https://YOUR-USERNAME.github.io/YOUR-REPO/
   ```

---

## 📁 File Structure

### For Local Development
```
project/
├── app.py                 # Flask application
├── autoencoder.py         # Python model
├── templates/
│   └── index.html        # Web interface
├── requirements.txt
└── ...
```

### For GitHub Pages
```
gh-pages/ (auto-generated or manual)
├── index.html            # Renamed from index-gh-pages.html
├── model_weights.json    # Pre-trained weights
├── js/
│   └── autoencoder.js    # JavaScript implementation
└── ...
```

---

## 🔧 How It Works on GitHub Pages

1. **Model Training** (happens locally):
   - Python script trains the autoencoder
   - Weights are exported to `model_weights.json`

2. **Frontend Execution** (happens in browser):
   - `autoencoder.js` implements the ML model in JavaScript
   - Loads pre-trained weights from `model_weights.json`
   - All computations run client-side in the browser

3. **No Backend Required**:
   - Pure static HTML/CSS/JavaScript
   - Works on any static hosting (GitHub Pages, Netlify, Vercel, etc.)
   - No Python dependencies needed in production

---

## 📊 Features Available on GitHub Pages

✅ **Fully Functional:**
- Model training simulation
- Anomaly detection
- Scenario simulation (normal, spike, drift, oscillation)
- Real-time charts and visualizations
- Metrics tracking

✅ **What's Different:**
- Uses JavaScript for ML computations (slightly slower, but sufficient for demo)
- Pre-trained weights loaded from JSON
- All processing happens in the browser

---

## 🚀 Using GitHub Actions for Auto-Deployment

The `.github/workflows/deploy.yml` file automates deployment:

```yaml
# Triggered on push to main/master
# 1. Exports model weights
# 2. Copies files to gh-pages directory
# 3. Deploys to GitHub Pages
```

**To use:**
1. Commit and push to your main branch:
   ```bash
   git push origin main
   ```

2. GitHub Actions automatically runs the workflow
3. Check the "Actions" tab in GitHub for build status
4. Your site updates at `https://YOUR-USERNAME.github.io/YOUR-REPO/`

---

## 🔗 Alternative Hosting Options

Besides GitHub Pages, use the same files on:

### Netlify
```bash
# Connect your GitHub repo
# Drag-and-drop gh-pages folder
# Or use Netlify CLI
netlify deploy --prod --dir=gh-pages
```

### Vercel
```bash
# Connect GitHub repo to Vercel
# Automatic deployments on push
```

### AWS S3 + CloudFront
```bash
aws s3 sync gh-pages/ s3://your-bucket/
```

### Any Web Server
- Copy `gh-pages/` contents to web root
- No special configuration needed

---

## 🛠️ Troubleshooting

### Site not appearing after push
- Check GitHub Actions workflow status
- Verify branch is set to `main` or `master`
- Wait 1-2 minutes for GitHub Pages to update

### Model weights not loading
- Ensure `model_weights.json` is in the same directory as `index.html`
- Check browser console for errors (F12)
- Verify file paths in `autoencoder.js`

### Slow performance on GitHub Pages
- This is expected for large datasets
- Use smaller sample sizes for training
- Simplify scenarios to reduce computation

### Issues with relative paths
- GitHub Pages might need URL adjustments if deployed to a subdirectory
- If site is at `github.io/repo-name/`, add base path configuration

---

## 📝 Configuration

### Modify Model Behavior
Edit `js/autoencoder.js`:
```javascript
// Change threshold sensitivity
this.threshold = 0.05; // Lower = more sensitive

// Adjust network architecture
this.n_features = 8; // Number of sensors
```

### Update Training Parameters
Edit `index-gh-pages.html`:
```html
<!-- Default training samples -->
<input type="number" id="nSamples" value="1000" min="100" max="5000">

<!-- Default epochs -->
<input type="number" id="epochs" value="50" min="10" max="200">
```

---

## 📦 Exporting for Other Platforms

To use this on other static hosting services:

```bash
# Create deployment package
mkdir -p deployment
cp index-gh-pages.html deployment/index.html
cp model_weights.json deployment/
cp -r js deployment/

# Now deploy the 'deployment' folder to your hosting
```

---

## 🎯 Quick Start

```bash
# 1. Export model
python export_model.py

# 2. Test locally (optional)
python app.py

# 3. Prepare deployment
mkdir -p gh-pages
cp index-gh-pages.html gh-pages/index.html
cp model_weights.json gh-pages/
cp -r js gh-pages/

# 4. Push to GitHub
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main

# 5. Access at https://YOUR-USERNAME.github.io/YOUR-REPO/
```

---

## 📞 Support

For issues:
1. Check browser console (F12) for JavaScript errors
2. Verify all files are present in deployment directory
3. Ensure model_weights.json is valid JSON
4. Review GitHub Actions logs for build errors

---

## ✨ Summary

- **Local**: `python app.py` → Full Python backend
- **GitHub Pages**: Push code → Auto-deploy static site
- **Performance**: Browser-based ML computations
- **Hosting**: Works anywhere static files are served

Your SENTINEL anomaly detection system is now deployment-ready! 🚀
