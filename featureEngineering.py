import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class InsuranceFeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        # Tidak ada yang perlu dipelajari dari data (stateless)
        # Return self agar bisa di-chain
        return self
    
    def transform(self, X):
        df = X.copy()
        
        # --- 1. Risk Level Logic ---
        conditions = [
            (df['smoker'] == 'yes') & (df['bmi'] > 30),
            (df['smoker'] == 'yes') & (df['bmi'] <= 30),
            (df['smoker'] == 'no') & (df['bmi'] > 30),
            (df['smoker'] == 'no') & (df['bmi'] <= 30)
        ]
        levels = [3, 2, 1, 0]
        df['risk_level'] = np.select(conditions, levels, default=0)
        
        # --- 2. BMI Category Logic ---
        def cat_bmi_logic(x):
            if x < 18.5: return 'Underweight'
            elif 18.5 <= x < 24.9: return 'Healthy weight'
            elif 25 <= x < 29.9: return 'Overweight'
            else: return 'Obesity'
            
        df['bmi_category'] = df['bmi'].apply(cat_bmi_logic)
        
        # --- 3. Smoker Binary Logic ---
        df['smoker'] = df['smoker'].apply(lambda x: 1 if x == 'yes' else 0)
        
        return df