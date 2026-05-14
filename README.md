# ChurnSense — Customer Churn Prediction App
### Full-Stack ML Web Application · Flask + Vanilla HTML/CSS/JS

---

## 📁 Folder Structure

```
churn_app/
├── app.py                 ← Flask backend (REST API)
├── requirements.txt       ← Python dependencies
├── churn_model.pkl        ← YOUR model (copy here, or set path)
└── frontend/
    └── index.html         ← Beautiful prediction UI
```

---

## ⚙️ STEP 1 — Set Up Python Environment

Open a terminal (Command Prompt or PowerShell on Windows):

```bash
# Navigate to the app folder
cd C:\path\to\churn_app

# (Optional but recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 📦 STEP 2 — Place Your Model

**Option A** (recommended): Copy your model file into the `churn_app/` folder:
```
C:\Users\inhaj\churn_model.pkl  →  churn_app\churn_model.pkl
```
Then edit `app.py` line 12:
```python
MODEL_PATH = os.environ.get("MODEL_PATH", "churn_model.pkl")
```

**Option B**: Keep the model at its original path. The default path in `app.py` is already set to:
```
C:\Users\inhaj\churn_model.pkl
```
No changes needed if you're running as the `inhaj` user.

**Option C**: Set an environment variable before running:
```bash
set MODEL_PATH=C:\Users\inhaj\churn_model.pkl   # Windows CMD
$env:MODEL_PATH="C:\Users\inhaj\churn_model.pkl" # PowerShell
```

---

## 🚀 STEP 3 — Run the Flask Backend

```bash
python app.py
```

You should see:
```
✅ Model loaded from: C:\Users\inhaj\churn_model.pkl
 * Running on http://127.0.0.1:5000
```

If you see `❌ Model not found`, re-check STEP 2.

---

## 🌐 STEP 4 — Open the Frontend

Open your browser and go to:
```
http://127.0.0.1:5000
```

The Flask server automatically serves the `frontend/index.html` file.

---

## 🔌 API Reference

### `POST /api/predict`
Send a JSON body with all 6 features:
```json
{
  "DayMins":         245.5,
  "MonthlyCharge":   65.40,
  "CustServCalls":   3,
  "OverageFee":      12.80,
  "RoamMins":        14.2,
  "ContractRenewal": 0
}
```

**Response:**
```json
{
  "prediction":  1,
  "label":       "CHURN",
  "churn_prob":  78.3,
  "stay_prob":   21.7,
  "risk":        "High Risk",
  "features":    { "DayMins": 245.5, ... }
}
```
- `prediction`: `1` = Churn, `0` = Stay
- `risk`: `"High Risk"` (≥70%), `"Medium Risk"` (40–69%), `"Low Risk"` (<40%)

### `GET /api/health`
Check server + model status:
```json
{ "status": "ok", "model_loaded": true, "model_path": "..." }
```

---

## 🧪 Test Without the UI (curl / Postman)

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d "{\"DayMins\":300,\"MonthlyCharge\":80,\"CustServCalls\":5,\"OverageFee\":15,\"RoamMins\":20,\"ContractRenewal\":0}"
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `❌ Model not found` | Check MODEL_PATH in app.py or set env variable |
| `Cannot reach server` in UI | Make sure `python app.py` is running |
| `AttributeError: predict_proba` | Your model doesn't support probabilities; prediction still works |
| CORS error in browser | Already handled via `flask-cors` |

---

## 🔮 Feature Reference

| Feature | Type | Description |
|---|---|---|
| `DayMins` | float | Total daytime minutes used |
| `MonthlyCharge` | float | Customer's monthly bill ($) |
| `CustServCalls` | int | Number of customer service calls |
| `OverageFee` | float | Charges beyond the plan limit ($) |
| `RoamMins` | float | Minutes used while roaming |
| `ContractRenewal` | 0 or 1 | Whether customer renewed contract |

---

## 🚢 Deploy to Production (optional)

Use **Gunicorn** (Linux/Mac) instead of Flask's dev server:
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

Or deploy to **Render / Railway / Heroku** by adding a `Procfile`:
```
web: gunicorn app:app
```
