# SENTINEL — Industrial Anomaly Detection System

Autoencoder-based anomaly detection for industrial sensor data using Flask + pure NumPy.

## Architecture

```
Input (8) → Encoder (4) → Latent (2) → Decoder (4) → Output (8)
```

Reconstruction loss (MSE) is minimized during training on normal data.
Anomalies are detected when reconstruction error exceeds the 95th percentile threshold.

## Sensors Monitored

| Sensor      | Unit  | Normal Range |
|-------------|-------|-------------|
| Temperature | °C    | 55–65       |
| Pressure    | bar   | 0.9–1.1     |
| RPM         | rpm   | 1450–1550   |
| Vibration   | mm/s  | 18–22       |
| Voltage     | V     | 215–225     |
| Current     | A     | 9–11        |
| Flow Rate   | L/min | 37–43       |
| Humidity    | %     | 45–55       |

## Setup & Run

```bash
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000

## API Endpoints

| Method | Endpoint       | Description                    |
|--------|----------------|--------------------------------|
| POST   | /api/train     | Train autoencoder              |
| POST   | /api/detect    | Detect anomaly in one reading  |
| POST   | /api/simulate  | Run scenario simulation        |
| GET    | /api/metrics   | Get system metrics             |
| POST   | /api/batch_detect | Batch anomaly detection     |

## Scenarios

- **Normal** — Baseline sensor operation
- **Overheat** — Temperature spike in second half
- **Vibration** — High-frequency vibration fault
- **Power Surge** — Random voltage/current spikes

## 🌐 GitHub Pages Deployment

This project now supports **deployment on GitHub Pages**!

### Deploy to GitHub Pages (No Backend Required)

```bash
# 1. Export model weights
python export_model.py

# 2. Run setup script
./setup-github-pages.sh  # macOS/Linux
setup-github-pages.bat   # Windows

# 3. Push to GitHub
git push origin main
```

Your site will be available at: `https://YOUR-USERNAME.github.io/YOUR-REPO/`

### Key Features:
- ✅ **Pure Frontend** — Runs entirely in the browser
- ✅ **No Backend Needed** — Perfect for GitHub Pages
- ✅ **JavaScript ML** — Pre-trained weights from Python model
- ✅ **Full Functionality** — Train, detect, simulate, visualize

### How It Works:
1. **Local**: Python trains the autoencoder
2. **Export**: Model weights → `model_weights.json`
3. **Frontend**: JavaScript loads and uses the weights
4. **Deploy**: Push to GitHub → Auto-deploy to Pages

📖 **Full deployment guide**: See [GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)

### Two Deployment Modes:

| Mode | Command | Deployment |
|------|---------|-----------|
| **Local** | `python app.py` | `http://localhost:5000` |
| **GitHub Pages** | `git push origin main` | `https://username.github.io/repo` |
