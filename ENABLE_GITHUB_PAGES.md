# 🚀 Enable GitHub Pages - Final Step

Your code is now on GitHub! Follow these steps to enable GitHub Pages:

## Option 1: Using GitHub Actions (Recommended - Automatic)

1. Go to your repository: `https://github.com/PranjalPratik/Autoencoder-to-detect-anomalies`
2. Click **Settings** (top right)
3. Scroll to **Pages** (left sidebar)
4. Under "Build and deployment":
   - Set **Source** to: `GitHub Actions`
5. That's it! GitHub Actions will auto-deploy on every push

✅ Your site will be live at: **`https://pranjalpratik.github.io/Autoencoder-to-detect-anomalies/`**

---

## Option 2: Manual Deployment (If GitHub Actions fails)

1. Go to your repository **Settings → Pages**
2. Under "Build and deployment":
   - Set **Source** to: `Deploy from a branch`
   - Set **Branch** to: `gh-pages` / `root`
3. Click **Save**

Then run locally:
```bash
cd e:\project
git subtree push --prefix gh-pages origin gh-pages
```

---

## Verify Deployment

1. Go to **Settings → Pages**
2. Look for the message: "Your site is live at: `https://pranjalpratik.github.io/Autoencoder-to-detect-anomalies/`"
3. Click the link to visit your live SENTINEL app!

---

## What's Deployed?

- ✅ `index.html` - Web UI
- ✅ `js/autoencoder.js` - JavaScript ML model
- ✅ `model_weights.json` - Pre-trained weights
- ✅ Full anomaly detection system (runs in browser)

---

## 🎉 You're All Set!

Your SENTINEL anomaly detection system is ready for:
- **Local testing**: `python app.py` → `http://localhost:5000`
- **Production**: GitHub Pages → `https://pranjalpratik.github.io/Autoencoder-to-detect-anomalies/`

Share your GitHub Pages link with anyone - no backend needed!
