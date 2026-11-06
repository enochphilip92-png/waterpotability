"""
Water Potability Preprocessing Pipeline
Author: URLA ENOCH PHILIP (Roll No: 23ME1A54B1)
Domain: Machine Learning & Predictive Analytics
Guide: Mr. E. Surendra babu

Handles:
- Missing value imputation
- Outlier management
- Feature scaling with StandardScaler (essential for SVM distance metrics)
- Train/Test stratification
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

FEATURE_COLUMNS = [
    'ph',
    'Hardness',
    'Solids',
    'Chloramines',
    'Sulfate',
    'Conductivity',
    'Organic_carbon',
    'Trihalomethanes',
    'Turbidity'
]

TARGET_COLUMN = 'Potability'

# WHO Recommended Permissible Drinking Water Quality Guidelines
WHO_GUIDELINES = {
    'ph': {'min': 6.5, 'max': 8.5, 'unit': 'pH', 'desc': 'Safe range is 6.5 to 8.5.'},
    'Hardness': {'min': 0.0, 'max': 300.0, 'unit': 'mg/L', 'desc': 'Acceptable limit < 300 mg/L (as CaCO3).'},
    'Solids': {'min': 0.0, 'max': 1000.0, 'unit': 'ppm', 'desc': 'Desirable limit < 500 ppm, permissible up to 1000 ppm.'},
    'Chloramines': {'min': 0.0, 'max': 4.0, 'unit': 'ppm', 'desc': 'WHO permissible limit <= 4.0 ppm.'},
    'Sulfate': {'min': 0.0, 'max': 250.0, 'unit': 'mg/L', 'desc': 'Permissible limit <= 250 mg/L.'},
    'Conductivity': {'min': 0.0, 'max': 400.0, 'unit': 'uS/cm', 'desc': 'Ideal EC < 400 uS/cm.'},
    'Organic_carbon': {'min': 0.0, 'max': 4.0, 'unit': 'ppm', 'desc': 'Permissible TOC < 4.0 ppm (clean water < 2 ppm).'},
    'Trihalomethanes': {'min': 0.0, 'max': 80.0, 'unit': 'ug/L', 'desc': 'Safe drinking limit <= 80 ug/L.'},
    'Turbidity': {'min': 0.0, 'max': 5.0, 'unit': 'NTU', 'desc': 'WHO limit <= 5.0 NTU (ideal < 1.0 NTU).'}
}

def load_data(filepath=None):
    """Load dataset from path or default data folder."""
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'water_potability.csv')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    return pd.read_csv(filepath)

def preprocess_and_split(df, test_size=0.2, random_state=42, save_artifacts=True, artifacts_dir=None):
    """
    Impute missing values with median, scale features, and perform stratified split.
    """
    if artifacts_dir is None:
        artifacts_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(artifacts_dir, exist_ok=True)
    
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    
    # 1. Stratified Split first to prevent data leakage from test to train set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # 2. Imputer (fitted strictly on train)
    imputer = SimpleImputer(strategy='median')
    X_train_imp = imputer.fit_transform(X_train)
    X_test_imp = imputer.transform(X_test)
    
    # 3. Scaler (fitted strictly on train)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_imp)
    X_test_scaled = scaler.transform(X_test_imp)
    
    # Save artifacts for inference
    if save_artifacts:
        imputer_path = os.path.join(artifacts_dir, 'imputer.pkl')
        scaler_path = os.path.join(artifacts_dir, 'scaler.pkl')
        joblib.dump(imputer, imputer_path)
        joblib.dump(scaler, scaler_path)
        print(f"Saved imputer to {imputer_path}")
        print(f"Saved scaler to {scaler_path}")
        
    return X_train_scaled, X_test_scaled, y_train, y_test, imputer, scaler

def transform_sample(sample_dict_or_df, artifacts_dir=None):
    """
    Transform raw incoming sample dictionary or DataFrame for inference.
    """
    if artifacts_dir is None:
        artifacts_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
    imputer_path = os.path.join(artifacts_dir, 'imputer.pkl')
    scaler_path = os.path.join(artifacts_dir, 'scaler.pkl')
    
    if not (os.path.exists(imputer_path) and os.path.exists(scaler_path)):
        raise FileNotFoundError("Preprocessor artifacts (imputer.pkl, scaler.pkl) missing. Run training first.")
        
    imputer = joblib.load(imputer_path)
    scaler = joblib.load(scaler_path)
    
    if isinstance(sample_dict_or_df, dict):
        df = pd.DataFrame([sample_dict_or_df])
    else:
        df = sample_dict_or_df.copy()
        
    # Ensure correct columns
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan
            
    df_ordered = df[FEATURE_COLUMNS]
    imputed = imputer.transform(df_ordered)
    scaled = scaler.transform(imputed)
    return scaled
