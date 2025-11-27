import joblib
import numpy as np
import pandas as pd

# Load model
with open('./models/best_model.pkl', 'rb') as f:
    model = joblib.load(f)

print(f"Model loaded: {type(model).__name__}")


def create_risk_levels(df):
    df = df.copy()
    
    # Risk level 0-3
    conditions = [
        (df['smoker'] == 'yes') & (df['bmi'] > 30),  # Level 3: Sangat tinggi
        (df['smoker'] == 'yes') & (df['bmi'] <= 30), # Level 2: Tinggi
        (df['smoker'] == 'no') & (df['bmi'] > 30),  # Level 1: Sedang
        (df['smoker'] == 'no') & (df['bmi'] <= 30)  # Level 0: Rendah
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

# Test prediction
data = {
    'age': 31,
    'sex': 'male',
    'bmi': 27.36,
    'children': 3,
    'smoker': 'no', 
    'region': 'northeast', 
    'charges': 1321.8739  
}

# Buat DataFrame
df_random = pd.DataFrame(data, index=[0])
df_random['bmi'] = df_random['bmi'].round(2)    
df_random['charges'] = df_random['charges'].round(4)
df_random['smoker'] = df_random['smoker'].apply(lambda x: 1 if x == 'yes' else 0)
df_random = create_risk_levels(df_random)
df_random['bmi_category'] = df_random['bmi'].apply(cat_bmi)

X_testnew = df_random.drop('charges', axis=1)
y_testnew = df_random['charges']

prediction = model.predict(X_testnew)
print(f"Test prediction: ${prediction[0]:,.2f}")