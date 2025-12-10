from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os
import numpy as np

try:
    from featureEngineering import InsuranceFeatureEngineer
except ImportError:
    pass # Abaikan jika tidak menggunakan file terpisah (tapi sangat disarankan)

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'best_model.pkl')

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded: {type(model).__name__} from {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'success': False, 'error': 'Model not loaded on server.'}), 500

    try:
        data = request.get_json(force=True)

        # 1. Siapkan Data Row (Sesuai variable Anda)
        row = {
            'age': int(data.get('age', 0)),
            'sex': data.get('sex', ''),
            'bmi': float(data.get('bmi', 0.0)),
            'children': int(data.get('children', 0)),
            'smoker': data.get('smoker', ''),
            'region': data.get('region', '')
        }

        # 2. Buat DataFrame Raw (Data Mentah)
        # Pipeline akan otomatis memproses feature engineering di dalam sini
        X = pd.DataFrame([row])
        
        # 3. Prediksi (Variable Anda)
        preds = model.predict(X)
        final_cost = float(preds[0])

        # --- LOGIKA TAMBAHAN UNTUK UI (BADGE) ---
        bmi_val = row['bmi']
        if bmi_val < 18.5: bmi_cat = 'Underweight'
        elif 18.5 <= bmi_val < 24.9: bmi_cat = 'Healthy weight'
        elif 25 <= bmi_val < 29.9: bmi_cat = 'Overweight'
        else: bmi_cat = 'Obesity'

        # Hitung Risk Level untuk UI
        smoker_val = row['smoker']
        if smoker_val == 'yes' and bmi_val > 30:
            risk_text = "Extreme Risk" # 3
            risk_val = 3
        elif smoker_val == 'yes' and bmi_val <= 30:
            risk_text = "High Risk" # 2
            risk_val = 2
        elif smoker_val == 'no' and bmi_val > 30:
            risk_text = "Medium Risk" # 1
            risk_val = 1
        else:
            risk_text = "Low Risk" # 0
            risk_val = 0

        return jsonify({
            'success': True, 
            'prediction': round(final_cost, 2), 
            'bmi_category': bmi_cat,
            'risk_level': risk_text,
            'risk_val': risk_val
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)