"""
Generate Realistic Water Quality Dataset with Physical-Chemical Water Quality Rules
Author: URLA ENOCH PHILIP (Roll No: 23ME1A54B1)
Domain: Machine Learning & Predictive Analytics
Guide: Mr. E. Surendra babu

Incorporates WHO drinking water standards:
- pH: Safe between 6.5 and 8.5
- Hardness: Safe under 250 mg/L
- Solids (TDS): Safe under 800 ppm (acceptable up to 1000 ppm)
- Chloramines: Safe under 4.0 ppm (WHO guideline)
- Sulfate: Safe under 250 mg/L
- Conductivity: Safe under 400 uS/cm
- Organic Carbon (TOC): Safe under 4.0 ppm
- Trihalomethanes: Safe under 80 ug/L
- Turbidity: Safe under 5.0 NTU
"""

import os
import numpy as np
import pandas as pd

def generate_realistic_water_dataset(n_samples=3276, random_state=42):
    np.random.seed(random_state)
    
    # 1. Generate realistic underlying parameter distributions
    ph = np.random.normal(loc=7.1, scale=1.3, size=n_samples)
    ph = np.clip(ph, 0.5, 13.5)
    
    hardness = np.random.normal(loc=195.0, scale=35.0, size=n_samples)
    hardness = np.clip(hardness, 50.0, 320.0)
    
    solids = np.random.exponential(scale=600.0, size=n_samples) + np.random.normal(loc=400.0, scale=200.0, size=n_samples)
    solids = np.clip(solids, 100.0, 2500.0)
    
    chloramines = np.random.normal(loc=3.8, scale=1.5, size=n_samples)
    chloramines = np.clip(chloramines, 0.2, 10.0)
    
    sulfate = np.random.normal(loc=230.0, scale=50.0, size=n_samples)
    sulfate = np.clip(sulfate, 50.0, 450.0)
    
    conductivity = np.random.normal(loc=380.0, scale=70.0, size=n_samples)
    conductivity = np.clip(conductivity, 150.0, 650.0)
    
    organic_carbon = np.random.normal(loc=4.5, scale=2.0, size=n_samples)
    organic_carbon = np.clip(organic_carbon, 0.5, 15.0)
    
    trihalomethanes = np.random.normal(loc=65.0, scale=20.0, size=n_samples)
    trihalomethanes = np.clip(trihalomethanes, 10.0, 130.0)
    
    turbidity = np.random.normal(loc=3.8, scale=1.2, size=n_samples)
    turbidity = np.clip(turbidity, 0.8, 8.5)
    
    # 2. Determine potability based on WHO non-linear thresholds + environmental noise
    # Calculate a composite penalty score for unsafe deviations
    penalty = np.zeros(n_samples)
    
    # pH outside 6.5 - 8.5
    ph_penalty = np.where(ph < 6.5, (6.5 - ph) * 1.5, 0) + np.where(ph > 8.5, (ph - 8.5) * 1.5, 0)
    
    # Turbidity > 5.0 NTU is high risk for microbial pathogens
    turb_penalty = np.where(turbidity > 5.0, (turbidity - 5.0) * 1.8, 0)
    
    # Solids (TDS) > 1000 ppm
    solids_penalty = np.where(solids > 1000.0, (solids - 1000.0) / 300.0, 0)
    
    # Chloramines > 4.0 ppm
    chlor_penalty = np.where(chloramines > 4.0, (chloramines - 4.0) * 1.2, 0)
    
    # Sulfate > 250 mg/L
    sulfate_penalty = np.where(sulfate > 250.0, (sulfate - 250.0) / 60.0, 0)
    
    # Organic carbon > 4.0 ppm
    toc_penalty = np.where(organic_carbon > 4.0, (organic_carbon - 4.0) * 1.1, 0)
    
    # Trihalomethanes > 80 ug/L
    thm_penalty = np.where(trihalomethanes > 80.0, (trihalomethanes - 80.0) / 20.0, 0)
    
    total_penalty = (
        ph_penalty * 1.2 +
        turb_penalty * 1.4 +
        solids_penalty * 0.9 +
        chlor_penalty * 1.0 +
        sulfate_penalty * 0.8 +
        toc_penalty * 0.9 +
        thm_penalty * 0.9
    )
    
    # Latent probability of being potable
    # Sigmoidal transition with realistic measurement noise
    noise = np.random.normal(0, 0.6, size=n_samples)
    z = 1.6 - total_penalty + noise
    prob_potable = 1.0 / (1.0 + np.exp(-z))
    
    potability = (prob_potable >= 0.50).astype(int)
    
    df = pd.DataFrame({
        'ph': np.round(ph, 3),
        'Hardness': np.round(hardness, 2),
        'Solids': np.round(solids, 2),
        'Chloramines': np.round(chloramines, 3),
        'Sulfate': np.round(sulfate, 2),
        'Conductivity': np.round(conductivity, 2),
        'Organic_carbon': np.round(organic_carbon, 3),
        'Trihalomethanes': np.round(trihalomethanes, 2),
        'Turbidity': np.round(turbidity, 3),
        'Potability': potability
    })
    
    # Introduce ~10-15% realistic missing values in lab-dependent features
    mask_ph = np.random.rand(n_samples) < 0.12
    mask_sulfate = np.random.rand(n_samples) < 0.18
    mask_thm = np.random.rand(n_samples) < 0.08
    
    df.loc[mask_ph, 'ph'] = np.nan
    df.loc[mask_sulfate, 'Sulfate'] = np.nan
    df.loc[mask_thm, 'Trihalomethanes'] = np.nan
    
    return df

if __name__ == '__main__':
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'water_potability.csv')
    batch_path = os.path.join(data_dir, 'sample_test_batch.csv')
    
    df = generate_realistic_water_dataset()
    df.to_csv(csv_path, index=False)
    # Save a slice for batch testing
    df.head(40).to_csv(batch_path, index=False)
    
    print(f"Dataset generated successfully at: {csv_path}")
    print(f"Total Rows: {len(df)}")
    print("Class Balance:")
    print(df['Potability'].value_counts())
    print("\nMissing Values:")
    print(df.isnull().sum())
