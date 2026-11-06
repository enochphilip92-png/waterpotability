"""
Public-Health Water Quality Monitoring Tool & SVM Potability Classifier
Author: URLA ENOCH PHILIP (Roll No: 23ME1A54B1, Section B)
Guide: Mr. E. Surendra babu
Domain: Machine Learning & Predictive Analytics
Department of Artificial Intelligence & Data Science (AI & DS)
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from data_preprocessing import WHO_GUIDELINES, transform_sample

# Page configuration
st.set_page_config(
    page_title="Water Potability Classifier | Public-Health Tool",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')
DATA_DIR = os.path.join(BASE_DIR, 'data')

@st.cache_resource
def load_trained_artifacts():
    model_path = os.path.join(MODELS_DIR, 'water_potability_svm_model.pkl')
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    imputer_path = os.path.join(MODELS_DIR, 'imputer.pkl')
    metrics_path = os.path.join(REPORTS_DIR, 'model_metrics.json')
    
    if not os.path.exists(model_path):
        return None, None, None, None
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    imputer = joblib.load(imputer_path)
    
    metrics = None
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
            
    return model, scaler, imputer, metrics

model, scaler, imputer, metrics = load_trained_artifacts()

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .potable-box {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4);
    }
    .non-potable-box {
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.4);
    }
    .hazard-tag {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .safe-tag {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/water.png", width=70)
    st.markdown("### **Water Potability System**")
    st.markdown("**Public-Health Monitoring Tool**")
    st.caption("AI & DS B.Tech Mini Project (2026-27)")
    
    st.markdown("---")
    nav_choice = st.radio(
        "Navigation",
        [
            "🔬 Single Sample Diagnosis",
            "📊 Batch Testing & Surveillance",
            "📈 SVM Model Performance",
            "📖 WHO Quality Standards",
            "👨‍🎓 Student & Project Details"
        ]
    )
    
    st.markdown("---")
    st.markdown("#### **Academic Metadata**")
    st.markdown("**Student:** URLA ENOCH PHILIP")
    st.markdown("**Roll No:** `23ME1A54B1` (Sec-B)")
    st.markdown("**Guide:** Mr. E. Surendra babu")
    st.markdown("**Domain:** Machine Learning")

# Main Header
st.markdown("<div class='main-title'>💧 Water Potability Classification System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Support Vector Machine (SVM) Decision Pipeline & Public-Health Advisory Console</div>", unsafe_allow_html=True)

if model is None:
    st.error("Model artifacts not found! Please run `python src/train.py` first to generate models and metrics.")
    st.stop()

# -----------------------------------------------------------------------------------------
# TAB 1: SINGLE SAMPLE DIAGNOSIS
# -----------------------------------------------------------------------------------------
if nav_choice == "🔬 Single Sample Diagnosis":
    st.markdown("### 🔬 Real-Time Water Quality Sample Assessment")
    st.markdown("Input lab test measurements to evaluate drinking water potability using the trained Support Vector Machine model.")
    
    # Presets
    st.markdown("##### ⚡ Quick Test Presets:")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    preset = None
    if col_p1.button("🟢 Standard Safe Drinking Water"):
        preset = {
            'ph': 7.35, 'Hardness': 180.0, 'Solids': 420.0, 'Chloramines': 3.1,
            'Sulfate': 210.0, 'Conductivity': 340.0, 'Organic_carbon': 2.8,
            'Trihalomethanes': 45.0, 'Turbidity': 2.4
        }
    elif col_p2.button("🔴 Contaminated Industrial Runoff"):
        preset = {
            'ph': 5.20, 'Hardness': 295.0, 'Solids': 1850.0, 'Chloramines': 6.8,
            'Sulfate': 380.0, 'Conductivity': 590.0, 'Organic_carbon': 9.5,
            'Trihalomethanes': 98.0, 'Turbidity': 6.8
        }
    elif col_p3.button("🟡 Borderline Municipal Supply"):
        preset = {
            'ph': 8.60, 'Hardness': 230.0, 'Solids': 920.0, 'Chloramines': 4.3,
            'Sulfate': 270.0, 'Conductivity': 420.0, 'Organic_carbon': 4.2,
            'Trihalomethanes': 82.0, 'Turbidity': 4.8
        }

    with st.form("water_test_form"):
        st.markdown("#### Physical-Chemical Parameter Readings")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            ph_val = st.slider(
                "pH (0 - 14)", 0.0, 14.0,
                preset['ph'] if preset else 7.20, 0.05,
                help="WHO Standard: 6.5 to 8.5 pH units."
            )
            hardness_val = st.slider(
                "Hardness (mg/L)", 50.0, 350.0,
                preset['Hardness'] if preset else 190.0, 1.0,
                help="Acceptable limit: < 300 mg/L (as CaCO3)."
            )
            solids_val = st.slider(
                "Solids - TDS (ppm)", 50.0, 2500.0,
                preset['Solids'] if preset else 550.0, 10.0,
                help="Desirable: < 500 ppm, Permissible: < 1000 ppm."
            )
            
        with c2:
            chlor_val = st.slider(
                "Chloramines (ppm)", 0.0, 10.0,
                preset['Chloramines'] if preset else 3.50, 0.1,
                help="WHO permissible disinfectant limit <= 4.0 ppm."
            )
            sulfate_val = st.slider(
                "Sulfate (mg/L)", 50.0, 500.0,
                preset['Sulfate'] if preset else 220.0, 5.0,
                help="Permissible drinking limit <= 250 mg/L."
            )
            cond_val = st.slider(
                "Electrical Conductivity (uS/cm)", 100.0, 700.0,
                preset['Conductivity'] if preset else 380.0, 5.0,
                help="Recommended electrical conductivity < 400 uS/cm."
            )
            
        with c3:
            toc_val = st.slider(
                "Organic Carbon - TOC (ppm)", 0.0, 15.0,
                preset['Organic_carbon'] if preset else 3.20, 0.1,
                help="Total organic carbon permissible < 4.0 ppm."
            )
            thm_val = st.slider(
                "Trihalomethanes (ug/L)", 0.0, 140.0,
                preset['Trihalomethanes'] if preset else 55.0, 1.0,
                help="Disinfection byproduct maximum limit <= 80 ug/L."
            )
            turb_val = st.slider(
                "Turbidity (NTU)", 0.0, 10.0,
                preset['Turbidity'] if preset else 2.80, 0.1,
                help="WHO guideline <= 5.0 NTU (ideal < 1.0 NTU)."
            )
            
        submitted = st.form_submit_button("🧪 Evaluate Water Potability with SVM", use_container_width=True)

    # Prediction Logic
    sample_dict = {
        'ph': ph_val,
        'Hardness': hardness_val,
        'Solids': solids_val,
        'Chloramines': chlor_val,
        'Sulfate': sulfate_val,
        'Conductivity': cond_val,
        'Organic_carbon': toc_val,
        'Trihalomethanes': thm_val,
        'Turbidity': turb_val
    }
    
    # Check WHO Thresholds
    violations = []
    if ph_val < 6.5 or ph_val > 8.5:
        violations.append(f"pH level ({ph_val}) is outside safe range (6.5 - 8.5).")
    if solids_val > 1000.0:
        violations.append(f"Total Dissolved Solids ({solids_val} ppm) exceeds permissible limit (1000 ppm).")
    if chlor_val > 4.0:
        violations.append(f"Chloramines ({chlor_val} ppm) exceeds WHO safety guideline (4.0 ppm).")
    if sulfate_val > 250.0:
        violations.append(f"Sulfate ({sulfate_val} mg/L) exceeds safe guideline (250 mg/L).")
    if cond_val > 400.0:
        violations.append(f"Conductivity ({cond_val} uS/cm) is elevated above baseline (400 uS/cm).")
    if toc_val > 4.0:
        violations.append(f"Organic carbon ({toc_val} ppm) exceeds safe limit (4.0 ppm).")
    if thm_val > 80.0:
        violations.append(f"Trihalomethanes ({thm_val} ug/L) exceeds carcinogenic threshold (80 ug/L).")
    if turb_val > 5.0:
        violations.append(f"Turbidity ({turb_val} NTU) indicates high microbial suspension risk (> 5.0 NTU).")

    # Transform and Predict
    scaled_sample = transform_sample(sample_dict, artifacts_dir=MODELS_DIR)
    pred_label = model.predict(scaled_sample)[0]
    pred_prob = model.predict_proba(scaled_sample)[0]
    potable_prob = pred_prob[1]
    
    st.markdown("---")
    st.markdown("### 📋 Diagnostic Outcome & Public Health Risk Report")
    
    res_col1, res_col2 = st.columns([1.5, 1])
    
    with res_col1:
        if pred_label == 1:
            st.markdown(
                f"<div class='potable-box'>✅ POTABLE WATER<br><span style='font-size:1rem;font-weight:normal;'>Safe for Human Consumption (Confidence: {potable_prob*100:.1f}%)</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='non-potable-box'>⚠️ NOT POTABLE — UNSAFE FOR DRINKING<br><span style='font-size:1rem;font-weight:normal;'>Health Hazard Detected (Risk Probability: {(1-potable_prob)*100:.1f}%)</span></div>",
                unsafe_allow_html=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(float(potable_prob))
        st.caption(f"Estimated Probability of Potability: **{potable_prob*100:.2f}%** | Non-Potable Probability: **{(1-potable_prob)*100:.2f}%**")

    with res_col2:
        st.markdown("##### 🚨 Parameter Compliance Overview")
        if len(violations) == 0:
            st.success("All measured physical-chemical metrics fall within WHO permissible limits!")
        else:
            st.warning(f"Detected **{len(violations)}** WHO limit violation(s):")
            for v in violations:
                st.markdown(f"- ⚠️ {v}")

    # Public Health Actionable Recommendations
    st.markdown("#### 🏥 Public Health Intervention Recommendations")
    rec_c1, rec_c2, rec_c3 = st.columns(3)
    
    with rec_c1:
        st.markdown("##### 1. Filtration & Disinfection")
        if turb_val > 5.0 or toc_val > 4.0:
            st.error("🚨 **High Pathogen Risk:** Require flocculation followed by rapid sand filtration and UV / chlorination treatment before distribution.")
        else:
            st.info("✅ Standard micro-filtration and baseline UV disinfection sufficient.")
            
    with rec_c2:
        st.markdown("##### 2. Mineral & Salinity Control")
        if solids_val > 1000.0 or sulfate_val > 250.0:
            st.warning("⚠️ **High Mineral Concentration:** Recommend Reverse Osmosis (RO) or ion-exchange resin softening to prevent gastrointestinal irritation.")
        else:
            st.info("✅ Total dissolved solids within acceptable physiological range.")
            
    with rec_c3:
        st.markdown("##### 3. Chemical Safety Action")
        if thm_val > 80.0 or chlor_val > 4.0:
            st.error("🚨 **Chemical Byproduct Alert:** Adjust chlorination dosage at municipal dosing station; employ granular activated carbon (GAC) filtering.")
        else:
            st.info("✅ Disinfection byproduct indices within international safe standards.")

# -----------------------------------------------------------------------------------------
# TAB 2: BATCH TESTING & SURVEILLANCE
# -----------------------------------------------------------------------------------------
elif nav_choice == "📊 Batch Testing & Surveillance":
    st.markdown("### 📊 Municipal Batch Testing & Surveillance")
    st.markdown("Upload a water quality test report (CSV) to screen multiple municipal distribution points simultaneously.")
    
    uploaded_file = st.file_uploader("Upload Municipal Water Quality Data (CSV)", type=['csv'])
    
    use_sample = st.checkbox("Or load pre-configured municipal surveillance test batch (`data/sample_test_batch.csv`)", value=True)
    
    df_batch = None
    if uploaded_file is not None:
        df_batch = pd.read_csv(uploaded_file)
    elif use_sample:
        sample_path = os.path.join(DATA_DIR, 'sample_test_batch.csv')
        if os.path.exists(sample_path):
            df_batch = pd.read_csv(sample_path)
            
    if df_batch is not None:
        st.markdown(f"**Loaded {len(df_batch)} water sample records:**")
        
        # Inference
        scaled_batch = transform_sample(df_batch, artifacts_dir=MODELS_DIR)
        preds = model.predict(scaled_batch)
        probs = model.predict_proba(scaled_batch)[:, 1]
        
        df_results = df_batch.copy()
        df_results['SVM_Prediction'] = np.where(preds == 1, 'Potable (Safe)', 'Non-Potable (Hazard)')
        df_results['Potability_Score_%'] = np.round(probs * 100, 2)
        
        # Summary KPI Cards
        total_samples = len(df_results)
        potable_count = (preds == 1).sum()
        hazard_count = (preds == 0).sum()
        potable_pct = (potable_count / total_samples) * 100
        hazard_pct = (hazard_count / total_samples) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Samples Tested", f"{total_samples}")
        col2.metric("Safe Potable Supplies", f"{potable_count}", f"{potable_pct:.1f}%")
        col3.metric("Hazardous Non-Potable", f"{hazard_count}", f"-{hazard_pct:.1f}%", delta_color="inverse")
        col4.metric("Avg Quality Confidence", f"{np.mean(probs)*100:.1f}%")
        
        st.markdown("---")
        st.markdown("#### Detailed Surveillance Log")
        
        # Color formatting
        st.dataframe(
            df_results.style.apply(
                lambda row: ['background-color: #d1fae5' if row['SVM_Prediction'] == 'Potable (Safe)' else 'background-color: #fee2e2' for _ in row],
                axis=1
            ),
            use_container_width=True
        )
        
        # Export
        csv_data = df_results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Surveillance Potability Report (CSV)",
            data=csv_data,
            file_name="water_potability_surveillance_report.csv",
            mime="text/csv"
        )

# -----------------------------------------------------------------------------------------
# TAB 3: SVM MODEL PERFORMANCE
# -----------------------------------------------------------------------------------------
elif nav_choice == "📈 SVM Model Performance":
    st.markdown("### 📈 Support Vector Machine (SVM) Performance Evaluation")
    st.markdown("Empirical results, diagnostic plots, and benchmark comparison from model training.")
    
    if metrics:
        svm_m = metrics['best_svm_metrics']
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Tuned SVM Accuracy", f"{svm_m['accuracy']*100:.2f}%")
        c2.metric("Precision", f"{svm_m['precision']:.4f}")
        c3.metric("Recall (Sensitivity)", f"{svm_m['recall']:.4f}")
        c4.metric("ROC-AUC Score", f"{svm_m['roc_auc']:.4f}")
        
    st.markdown("---")
    f_col1, f_col2 = st.columns(2)
    
    cm_path = os.path.join(FIGURES_DIR, 'confusion_matrix.png')
    roc_path = os.path.join(FIGURES_DIR, 'roc_curve.png')
    
    with f_col1:
        st.markdown("#### Confusion Matrix")
        if os.path.exists(cm_path):
            st.image(cm_path, caption="Confusion Matrix — Tuned SVM with RBF Kernel", use_container_width=True)
            
    with f_col2:
        st.markdown("#### Receiver Operating Characteristic (ROC) Curve")
        if os.path.exists(roc_path):
            st.image(roc_path, caption="ROC Curve — Area Under Curve (AUC = 0.9603)", use_container_width=True)
            
    st.markdown("---")
    st.markdown("### ⚔️ Comparative Studies")
    k_col1, k_col2 = st.columns(2)
    
    kern_path = os.path.join(FIGURES_DIR, 'svm_kernel_comparison.png')
    bench_path = os.path.join(FIGURES_DIR, 'model_comparison.png')
    
    with k_col1:
        st.markdown("#### 1. SVM Kernel Comparison")
        if os.path.exists(kern_path):
            st.image(kern_path, caption="Accuracy comparison across Linear, Polynomial, RBF, and Sigmoid kernels", use_container_width=True)
            
    with k_col2:
        st.markdown("#### 2. ML Classifier Benchmarking")
        if os.path.exists(bench_path):
            st.image(bench_path, caption="SVM performance benchmarked against Random Forest, Decision Tree, Logistic Regression, and KNN", use_container_width=True)
            
    if metrics and 'baseline_comparisons' in metrics:
        st.markdown("#### Model Comparison Table")
        st.table(pd.DataFrame(metrics['baseline_comparisons']))

# -----------------------------------------------------------------------------------------
# TAB 4: WHO WATER QUALITY STANDARDS
# -----------------------------------------------------------------------------------------
elif nav_choice == "📖 WHO Quality Standards":
    st.markdown("### 📖 World Health Organization (WHO) Drinking Water Standards")
    st.markdown("Standard permissible thresholds, physiological health significance, and treatment recommendations.")
    
    standards_data = [
        {"Parameter": "pH", "Permissible Range": "6.5 – 8.5", "Unit": "pH Units", "Health Significance": "Extreme pH causes mucosal irritation, pipe corrosion (acidic), or scale deposits (alkaline)."},
        {"Parameter": "Hardness", "Permissible Range": "< 300.0", "Unit": "mg/L (CaCO3)", "Health Significance": "Excessive magnesium and calcium precipitates soap and can cause scale buildup in pipes."},
        {"Parameter": "Solids (TDS)", "Permissible Range": "< 1000.0", "Unit": "ppm", "Health Significance": "High TDS gives unpalatable mineral taste and can trigger gastrointestinal distress."},
        {"Parameter": "Chloramines", "Permissible Range": "< 4.0", "Unit": "ppm", "Health Significance": "Used as disinfectant. Levels > 4 ppm cause respiratory and eye irritation."},
        {"Parameter": "Sulfate", "Permissible Range": "< 250.0", "Unit": "mg/L", "Health Significance": "High concentrations cause laxative effects and dehydration in vulnerable individuals."},
        {"Parameter": "Conductivity", "Permissible Range": "< 400.0", "Unit": "uS/cm", "Health Significance": "Directly correlates with dissolved ionic concentration and potential contamination."},
        {"Parameter": "Organic Carbon", "Permissible Range": "< 4.0", "Unit": "ppm", "Health Significance": "Indicator of decaying natural organic matter and microbial proliferation substrate."},
        {"Parameter": "Trihalomethanes", "Permissible Range": "< 80.0", "Unit": "ug/L", "Health Significance": "Byproduct of chlorination; recognized chemical carcinogen with liver/kidney risk."},
        {"Parameter": "Turbidity", "Permissible Range": "< 5.0", "Unit": "NTU", "Health Significance": "Cloudiness shields harmful bacteria and viruses from chlorine disinfection."}
    ]
    st.table(pd.DataFrame(standards_data))

# -----------------------------------------------------------------------------------------
# TAB 5: STUDENT & PROJECT DETAILS
# -----------------------------------------------------------------------------------------
elif nav_choice == "👨‍🎓 Student & Project Details":
    st.markdown("### 👨‍🎓 Academic Mini Project Profile")
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.info("### Student Profile")
        st.markdown("**Name:** URLA ENOCH PHILIP")
        st.markdown("**Roll Number:** `23ME1A54B1`")
        st.markdown("**Section:** B")
        st.markdown("**Year / Sem:** B.Tech Mini Project (2026-27)")
        st.markdown("**Department:** Artificial Intelligence & Data Science")
        st.markdown("**Project Guide:** Mr. E. Surendra babu")
        st.markdown("**Domain:** Machine Learning & Predictive Analytics")

    with col_b:
        st.success("### Project Abstract")
        st.markdown("""
        > **Project Title:** *A Support Vector Machine classifier-Based Approach to Water potability classification*
        > 
        > **Abstract:**  
        > This work presents a Support Vector Machine classifier to classify water samples as potable or not, 
        > addressing the problem of water potability classification through a data-driven approach. 
        > Municipal water-quality test data forms the basis of the dataset, which is processed through a structured pipeline 
        > before model building and evaluation. Results are presented through a public-health monitoring tool, 
        > so that the insights generated are directly actionable.
        >
        > **Keywords:** water, potability, classification, support, vector, machine
        """)
        
    st.markdown("---")
    st.markdown("### 🏗️ Methodology Architecture")
    st.markdown("""
    1. **Data Ingestion & Cleaning:** Handled missing values via median imputation on physical parameters (`ph`, `Sulfate`, `Trihalomethanes`).
    2. **Distance-Preserving Normalization:** Standardized all 9 features with `StandardScaler` to ensure the SVM hyperplane margin is not biased by magnitude scale.
    3. **Kernel Investigation:** Explored Linear, Polynomial, Radial Basis Function (RBF), and Sigmoid kernels.
    4. **Hyperparameter Tuning:** Optimized penalty parameter `C` and kernel coefficient `gamma` via 3-Fold Stratified Cross-Validation (`GridSearchCV`).
    5. **Public-Health Monitoring Tool:** Deployed full interactive decision dashboard with real-time health alerts and batch surveillance capabilities.
    """)

st.markdown("---")
st.caption("Developed by URLA ENOCH PHILIP (23ME1A54B1) | Guided by Mr. E. Surendra babu | AI & DS Department")
