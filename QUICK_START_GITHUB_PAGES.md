# 🚀 Quick Start — GitHub Pages Deployment

## ⚡ 30-Second Setup

```bash
# Step 1: Export model
python export_model.py

# Step 2: Windows users run this
setup-github-pages.bat

# OR Mac/Linux users run this
chmod +x setup-github-pages.sh
./setup-github-pages.sh

# Step 3: Push to GitHub
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

## ✨ Your site is live!

Visit: `https://YOUR-USERNAME.github.io/YOUR-REPO/`

---

## 📋 What Happened?

1. ✅ Model weights exported to `model_weights.json`
2. ✅ Files copied to `gh-pages/` directory
3. ✅ GitHub Actions configured (if using `.github/workflows/deploy.yml`)
4. ✅ Site deployed to GitHub Pages

---

## 📁 Files Created for GitHub Pages

```
NEW FILES:
├── js/autoencoder.js              ← JavaScript ML implementation
├── index-gh-pages.html            ← Standalone version (no Flask needed)
├── model_weights.json             ← Pre-trained weights
├── export_model.py                ← Export Python model to JSON
├── setup-github-pages.bat         ← Windows setup script
├── setup-github-pages.sh          ← Mac/Linux setup script
├── .github/workflows/deploy.yml   ← Automatic deployment config
├── GITHUB_PAGES_DEPLOYMENT.md     ← Full deployment guide
└── .gitignore                     ← Updated for GitHub Pages
```

---

## 🎯 Two Ways to Use Your Project

### Local Development (with Python backend)
```bash
python app.py
# → http://localhost:5000
# Full Flask backend with API
```

### Production (GitHub Pages - no backend)
```bash
git push origin main
# → https://YOUR-USERNAME.github.io/YOUR-REPO/
# Pure frontend, runs in browser
```

---

## 🔍 How It Works on GitHub Pages

**Python Side (One-time):**
- `export_model.py` trains the autoencoder
- Exports weights to `model_weights.json`

**Frontend Side (Every Visit):**
- `index.html` loads in browser
- JavaScript loads `model_weights.json`
- All ML computations happen client-side
- No backend required!

---

## ⚙️ Automatic Deployment

If you included `.github/workflows/deploy.yml`:

```bash
# Simply push code
git push origin main

# GitHub Actions automatically:
# 1. Trains model
# 2. Exports weights
# 3. Builds site
# 4. Deploys to GitHub Pages
```

Check the **"Actions"** tab in GitHub to see build status.

---

## 🚨 Troubleshooting

### Site not showing?
```bash
# Go to repository Settings → Pages
# Verify deployment source is set to:
# - "GitHub Actions" OR
# - Branch "gh-pages" (if manual)
```

### Model not loading?
```bash
# Check browser console: Press F12
# Look for errors about model_weights.json
# Verify file exists in gh-pages/ directory
```

### Setup script didn't work?
```bash
# Manual method:
mkdir -p gh-pages
cp index-gh-pages.html gh-pages/index.html
cp model_weights.json gh-pages/
cp -r js gh-pages/
```

---

## 📖 More Information

- **Full Guide**: [GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)
- **API Reference**: See `app.py` for local Flask endpoints
- **Configuration**: Edit `js/autoencoder.js` to tune model behavior

---

## ✅ Checklist

- [ ] Ran `python export_model.py`
- [ ] Ran setup script (`.bat` or `.sh`)
- [ ] Pushed to GitHub (`git push origin main`)
- [ ] Site is live at `https://YOUR-USERNAME.github.io/YOUR-REPO/`
- [ ] Test model training in browser
- [ ] Test anomaly detection
- [ ] Share your SENTINEL deployment! 🎉

---

**That's it! Your anomaly detection system is now deployed on GitHub Pages!** 🚀
