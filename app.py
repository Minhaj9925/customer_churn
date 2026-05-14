from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import joblib
import numpy as np
import pandas as pd
import os
import io

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

MODEL_PATH = os.environ.get("MODEL_PATH", r"churn_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded from: {MODEL_PATH}")
except FileNotFoundError:
    print(f"❌ Model not found at: {MODEL_PATH}")
    model = None

FEATURES = ['DayMins', 'MonthlyCharge', 'CustServCalls', 'OverageFee', 'RoamMins', 'ContractRenewal']


@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


def make_risk(cp):
    return "High Risk" if cp >= 70 else ("Medium Risk" if cp >= 40 else "Low Risk")


def get_proba(X):
    try:
        probas = model.predict_proba(X)
        return [round(float(p[1]) * 100, 1) for p in probas], [round(float(p[0]) * 100, 1) for p in probas]
    except AttributeError:
        preds = model.predict(X).tolist()
        cp = [100.0 if p == 1 else 0.0 for p in preds]
        return cp, [100.0 - c for c in cp]


@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded."}), 503
    data = request.get_json(force=True)
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    try:
        values = [float(data[f]) for f in FEATURES]
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid value: {e}"}), 400

    X = np.array(values).reshape(1, -1)
    prediction = int(model.predict(X)[0])
    churn_probs, stay_probs = get_proba(X)
    cp, sp = churn_probs[0], stay_probs[0]

    return jsonify({
        "prediction": prediction,
        "label":      "CHURN" if prediction == 1 else "STAY",
        "churn_prob": cp,
        "stay_prob":  sp,
        "risk":       make_risk(cp),
        "features":   dict(zip(FEATURES, values))
    })


@app.route('/api/predict_csv', methods=['POST'])
def predict_csv():
    if model is None:
        return jsonify({"error": "Model not loaded."}), 503
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    file = request.files['file']
    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "Only CSV files are supported."}), 400

    try:
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    except Exception as e:
        return jsonify({"error": f"Could not parse CSV: {e}"}), 400

    missing_cols = [f for f in FEATURES if f not in df.columns]
    if missing_cols:
        return jsonify({"error": f"Missing columns: {missing_cols}", "found": list(df.columns)}), 400

    try:
        X = df[FEATURES].astype(float).values
    except Exception as e:
        return jsonify({"error": f"Non-numeric data: {e}"}), 400

    predictions   = model.predict(X).tolist()
    churn_probs, stay_probs = get_proba(X)

    results = []
    for i, (pred, cp, sp) in enumerate(zip(predictions, churn_probs, stay_probs)):
        row = {col: (int(df[col].iloc[i]) if col in ['CustServCalls', 'ContractRenewal']
                     else round(float(df[col].iloc[i]), 2)) for col in FEATURES}
        row.update({
            "row": i + 1, "prediction": int(pred),
            "label": "CHURN" if pred == 1 else "STAY",
            "churn_prob": cp, "stay_prob": sp, "risk": make_risk(cp)
        })
        results.append(row)

    total     = len(results)
    churned   = sum(1 for r in results if r['prediction'] == 1)
    avg_churn = round(sum(r['churn_prob'] for r in results) / total, 1) if total else 0

    return jsonify({
        "total": total, "churned": churned, "staying": total - churned,
        "avg_churn_prob": avg_churn,
        "high_risk": sum(1 for r in results if r['risk'] == 'High Risk'),
        "med_risk":  sum(1 for r in results if r['risk'] == 'Medium Risk'),
        "low_risk":  sum(1 for r in results if r['risk'] == 'Low Risk'),
        "results": results
    })


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None, "model_path": MODEL_PATH})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)