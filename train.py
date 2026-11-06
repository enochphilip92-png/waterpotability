"""
Support Vector Machine (SVM) Training Pipeline
Author: URLA ENOCH PHILIP (Roll No: 23ME1A54B1)
Domain: Machine Learning & Predictive Analytics
Guide: Mr. E. Surendra babu

Trains:
1. Multiple SVM Kernels (Linear, Polynomial, RBF, Sigmoid)
2. Hyperparameter Optimization (GridSearchCV on C & Gamma)
3. Baseline Model Benchmark (Logistic Regression, Decision Tree, Random Forest, KNN)
4. Saves final production model, scaler, and performance metrics
"""

import os
import sys
import json
import joblib
import tempfile
import numpy as np
import pandas as pd

# Set writable matplotlib config dir
os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'mpl_cache')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from data_preprocessing import load_data, preprocess_and_split
from evaluate import evaluate_classifier

def run_pipeline():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    models_dir = os.path.join(project_root, 'models')
    reports_dir = os.path.join(project_root, 'reports')
    figures_dir = os.path.join(reports_dir, 'figures')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    
    print("=" * 70, flush=True)
    print("WATER POTABILITY CLASSIFICATION USING SUPPORT VECTOR MACHINE (SVM)", flush=True)
    print("Student: URLA ENOCH PHILIP | Roll No: 23ME1A54B1 | Guide: Mr. E. Surendra babu", flush=True)
    print("=" * 70, flush=True)
    
    # 1. Load and Preprocess Data
    print("\n[Step 1/5] Loading and Preprocessing Municipal Water Quality Data...", flush=True)
    df = load_data()
    print(f"Total dataset shape: {df.shape[0]} rows, {df.shape[1]} columns", flush=True)
    
    X_train, X_test, y_train, y_test, imputer, scaler = preprocess_and_split(
        df, test_size=0.2, random_state=42, save_artifacts=True, artifacts_dir=models_dir
    )
    print(f"Train samples: {X_train.shape[0]} | Test samples: {X_test.shape[0]}", flush=True)
    
    # 2. Kernel Comparative Study
    print("\n[Step 2/5] Comparative Study Across SVM Kernels...", flush=True)
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    kernel_results = {}
    
    for k in kernels:
        print(f"  -> Training SVM with kernel='{k}'...", flush=True)
        svm_temp = SVC(kernel=k, class_weight='balanced', probability=True, random_state=42)
        svm_temp.fit(X_train, y_train)
        y_pred = svm_temp.predict(X_test)
        y_prob = svm_temp.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)
        
        kernel_results[k] = {
            'accuracy': round(float(acc), 4),
            'f1_score': round(float(f1), 4),
            'roc_auc': round(float(auc), 4)
        }
        print(f"     Accuracy: {acc*100:.2f}% | F1: {f1:.4f} | ROC-AUC: {auc:.4f}", flush=True)
        
    # Plot Kernel Comparison
    plt.figure(figsize=(8, 4.5))
    kernel_names = [k.capitalize() for k in kernels]
    accs = [kernel_results[k]['accuracy'] * 100 for k in kernels]
    bars = plt.bar(kernel_names, accs, color=['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728'], width=0.55)
    plt.ylabel('Accuracy (%)', fontsize=11)
    plt.title('SVM Classification Accuracy Across Different Kernels', fontsize=12, fontweight='bold', pad=10)
    plt.ylim([50, 100])
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, h + 0.8, f'{h:.2f}%', ha='center', va='bottom', fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'svm_kernel_comparison.png'), dpi=300)
    plt.close()
    
    # 3. Hyperparameter Tuning on Best Kernel (RBF)
    print("\n[Step 3/5] Hyperparameter Optimization (GridSearchCV on RBF Kernel)...", flush=True)
    param_grid = {
        'C': [0.5, 1.0, 3.0],
        'gamma': ['scale', 'auto', 0.1],
        'kernel': ['rbf']
    }
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    grid_search = GridSearchCV(
        SVC(class_weight='balanced', probability=True, random_state=42),
        param_grid,
        cv=cv,
        scoring='f1',
        n_jobs=1,
        verbose=1
    )
    grid_search.fit(X_train, y_train)
    best_svm = grid_search.best_estimator_
    print(f"  -> Best Hyperparameters: {grid_search.best_params_}", flush=True)
    print(f"  -> Best Cross-Validation Accuracy: {grid_search.best_score_*100:.2f}%", flush=True)
    
    # 4. Comprehensive Evaluation of Tuned SVM
    print("\n[Step 4/5] Evaluating Tuned SVM on Held-Out Test Set...", flush=True)
    best_metrics = evaluate_classifier(
        best_svm, X_test, y_test, model_name="Tuned SVM (RBF Kernel)", output_dir=reports_dir
    )
    print(f"  Test Accuracy : {best_metrics['accuracy'] * 100:.2f}%", flush=True)
    print(f"  Test Precision: {best_metrics['precision']:.4f}", flush=True)
    print(f"  Test Recall   : {best_metrics['recall']:.4f}", flush=True)
    print(f"  Test F1-Score : {best_metrics['f1_score']:.4f}", flush=True)
    print(f"  Test ROC-AUC  : {best_metrics['roc_auc']:.4f}", flush=True)
    
    # Save best model
    model_path = os.path.join(models_dir, 'water_potability_svm_model.pkl')
    joblib.dump(best_svm, model_path)
    print(f"\nSaved optimal SVM model to: {model_path}", flush=True)
    
    # 5. Baseline Comparison with Other ML Classifiers
    print("\n[Step 5/5] Benchmarking SVM against Baseline ML Classifiers...", flush=True)
    baseline_models = {
        'Support Vector Machine (Tuned)': best_svm,
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=6, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=7)
    }
    
    benchmark_results = []
    for name, model in baseline_models.items():
        if name != 'Support Vector Machine (Tuned)':
            model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        if hasattr(model, 'predict_proba'):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = y_pred
            
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        try:
            auc = roc_auc_score(y_test, y_prob)
        except Exception:
            auc = 0.5
            
        benchmark_results.append({
            'Model': name,
            'Accuracy': round(float(acc), 4),
            'Precision': round(float(prec), 4),
            'Recall': round(float(rec), 4),
            'F1_Score': round(float(f1), 4),
            'ROC_AUC': round(float(auc), 4)
        })
        
    benchmark_df = pd.DataFrame(benchmark_results)
    print("\n" + benchmark_df.to_string(index=False), flush=True)
    
    # Plot Benchmark Comparison
    plt.figure(figsize=(10, 5))
    df_plot = benchmark_df.sort_values(by='Accuracy', ascending=False)
    palette = ['#1f77b4' if 'SVM' in m else '#aec7e8' for m in df_plot['Model']]
    sns.barplot(x='Accuracy', y='Model', hue='Model', data=df_plot, palette=palette, legend=False)
    plt.title('Benchmark Comparison of ML Classifiers for Water Potability', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Accuracy', fontsize=11)
    plt.ylabel('')
    for idx, row in df_plot.reset_index().iterrows():
        plt.text(row['Accuracy'] + 0.008, idx, f"{row['Accuracy']*100:.2f}%", va='center', fontweight='bold')
    plt.xlim([0.45, 0.95])
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'model_comparison.png'), dpi=300)
    plt.close()
    
    # Save all summary files
    summary_data = {
        'student_info': {
            'name': 'URLA ENOCH PHILIP',
            'roll_no': '23ME1A54B1',
            'guide': 'Mr. E. Surendra babu',
            'domain': 'Machine Learning & Predictive Analytics',
            'project_title': 'A Support Vector Machine classifier-Based Approach to Water potability classification'
        },
        'best_hyperparameters': grid_search.best_params_,
        'best_svm_metrics': best_metrics,
        'kernel_comparisons': kernel_results,
        'baseline_comparisons': benchmark_results
    }
    
    with open(os.path.join(reports_dir, 'model_metrics.json'), 'w') as f:
        json.dump(summary_data, f, indent=4)
    with open(os.path.join(models_dir, 'model_metrics.json'), 'w') as f:
        json.dump(summary_data, f, indent=4)
        
    print(f"\nMetrics and comparisons successfully saved to {os.path.join(reports_dir, 'model_metrics.json')}", flush=True)
    print("Training pipeline finished successfully!", flush=True)

if __name__ == '__main__':
    run_pipeline()
