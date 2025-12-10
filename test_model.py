import joblib
import numpy as np
import pandas as pd
# from featureEngineering import InsuranceFeatureEngineer

# Load model
with open('./models/best_model.pkl', 'rb') as f:
    model = joblib.load(f)

preprocessor_step = model.named_steps['preprocess']

# Lihat daftar transformers yang tersimpan di dalamnya
# print("Daftar kolom yang diingat oleh model:")
# for name, transformer, columns in preprocessor_step.transformers_:
#     print(f"Name: {name}")
#     print(f"Columns: {columns}")
#     print("-" * 20)

# Test prediction
data = {
    'age': 31,
    'sex': 'female',
    'bmi': 59.36,
    'children': 3,
    'smoker': 'yes', 
    'region': 'northeast', 
    'charges': 1321.8739  
}

# Buat DataFrame
df_random = pd.DataFrame(data, index=[0])

X_testnew = df_random.drop('charges', axis=1)
y_testnew = df_random['charges']

prediction = model.predict(X_testnew)
print(f"Test prediction: ${prediction[0]:,.2f}\nActual: ${y_testnew[0]:,.2f}")