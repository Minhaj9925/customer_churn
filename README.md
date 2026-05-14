# 🔄 Customer Churn Prediction System

A Machine Learning-powered web application that predicts whether a customer is likely to churn or stay — with real-time risk categorization and an intuitive web interface.

---

## 📌 Overview

Customer churn is one of the most critical challenges for businesses. This project uses a trained Machine Learning model integrated with a Flask backend to predict churn risk based on customer data. The system categorizes each prediction into actionable risk levels, helping businesses proactively retain customers before they leave.

---

## ✨ Features

- **Real-time churn prediction** — instant results powered by a trained ML model
- **Risk categorization** — customers are classified as:
  - 🔴 High Risk
  - 🟡 Medium Risk
  - 🟢 Likely to Stay
- **Interactive web interface** — clean, responsive frontend built with HTML, CSS, and JavaScript
- **Imbalanced data handling** — uses SMOTE to improve prediction on minority class (churners)
- **Flask REST backend** — lightweight API serving predictions on demand

---

## 🛠️ Technologies Used

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Machine Learning | Scikit-learn, Pandas, NumPy |
| Data Balancing | imbalanced-learn (SMOTE) |
| Frontend | HTML, CSS, JavaScript |
| Model Storage | Pickle (`.pkl`) |

---

## 📁 Project Structure

```
churn_app/
│
├── frontend/
│   └── index.html          # Main UI for prediction input & results
│
├── app.py                  # Flask app — API routes & model inference
├── churn_model.pkl         # Trained & serialized ML model
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🤖 Machine Learning Workflow

```
Raw Data
   │
   ▼
Data Preprocessing        ← Handle missing values, encode categoricals
   │
   ▼
Feature Engineering       ← Select & transform relevant features
   │
   ▼
SMOTE Oversampling         ← Balance imbalanced classes
   │
   ▼
Model Training             ← Train classifier with Scikit-learn
   │
   ▼
Evaluation                 ← Accuracy, Recall, Confusion Matrix
   │
   ▼
Serialization              ← Save model as churn_model.pkl
   │
   ▼
Flask Deployment           ← Serve predictions via REST API
```

---

## 📊 Model Performance

| Metric | Score |
|---|---|
| Accuracy | **80%** |
| Recall (Churn class) | **81%** |

> **Why Recall matters here:** In churn prediction, missing an actual churner (false negative) is more costly than a false alarm. The model is optimized for high recall to catch at-risk customers.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/churn_app.git
cd churn_app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Flask app
python app.py
```

### Usage

1. Open your browser and go to `http://127.0.0.1:5000`
2. Enter the customer details in the form
3. Click **Predict** to get an instant churn risk result

---

## 📦 Requirements

Key dependencies (see `requirements.txt` for full list):

```
flask
scikit-learn
pandas
numpy
imbalanced-learn
```

---

## 🔮 Future Improvements

- [ ] Add model retraining pipeline with new data
- [ ] Include SHAP-based feature importance explanations
- [ ] Add database integration for storing prediction history
- [ ] Deploy on cloud (AWS / Heroku / Render)
- [ ] Add user authentication for multi-user access

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).