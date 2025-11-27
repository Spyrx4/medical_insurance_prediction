from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os
import numpy as np

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

        def create_risk_levels(df):
            df = df.copy()

            # Risk level 0-3
            conditions = [
                (df['smoker'] == 'yes') & (df['bmi'] > 30),  
                (df['smoker'] == 'yes') & (df['bmi'] <= 30),
                (df['smoker'] == 'no') & (df['bmi'] > 30),  
                (df['smoker'] == 'no') & (df['bmi'] <= 30)
            ]

            levels = [3, 2, 1, 0]

            df['risk_level'] = np.select(conditions, levels, default=0)

            return df

        def cat_bmi(bmi):
            if bmi < 18.5:
                return 'Underweight'
            elif 18.5 <= bmi < 24.9:
                return 'Healthy weight'
            elif 25 <= bmi < 29.9:
                return 'Overweight'
            else:
                return 'Obesity'

        row = {
            'age': int(data.get('age', 0)),
            'sex': data.get('sex', ''),
            'bmi': float(data.get('bmi', 0.0)),
            'children': int(data.get('children', 0)),
            'smoker': data.get('smoker', ''),
            'region': data.get('region', '')
        }
        X = pd.DataFrame([row])
        X['smoker'] = X['smoker'].apply(lambda x: 1 if x == 'yes' else 0)
        X = create_risk_levels(X)
        X['bmi_category'] = X['bmi'].apply(cat_bmi)

        preds = model.predict(X)
        final_cost = float(preds[0])

        return jsonify({'success': True, 'cost': round(final_cost, 2)})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
