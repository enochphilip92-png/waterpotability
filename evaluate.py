"""
Model Evaluation and Visualization Module
Author: URLA ENOCH PHILIP (Roll No: 23ME1A54B1)
Domain: Machine Learning & Predictive Analytics
Guide: Mr. E. Surendra babu

Calculates:
- Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Generates publication-ready figures for project reports
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report
)

def evaluate_classifier(model, X_test, y_test, model_name="SVM (RBF Kernel)", output_dir=None):
    """
    Computes comprehensive classification metrics and saves diagnostic plots.
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    fig_dir = os.path.join(output_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    
    # Predictions
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        # Scale decision function to [0, 1] using sigmoid
        y_prob = 1 / (1 + np.exp(-model.decision_function(X_test)))
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
        
    cm = confusion_matrix(y_test, y_pred)
    report_dict = classification_report(y_test, y_pred, target_names=["Non-Potable", "Potable"], output_dict=True)
    
    metrics = {
        'model_name': model_name,
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall': round(float(rec), 4),
        'f1_score': round(float(f1), 4),
        'roc_auc': round(float(auc), 4),
        'confusion_matrix': cm.tolist(),
        'classification_report': report_dict
    }
    
    # 1. Confusion Matrix Plot
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=['Non-Potable (0)', 'Potable (1)'],
        yticklabels=['Non-Potable (0)', 'Potable (1)'],
        cbar=False, annot_kws={"size": 14, "weight": "bold"}
    )
    plt.title(f'Confusion Matrix — {model_name}', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Predicted Label', fontsize=11)
    plt.ylabel('Actual Label', fontsize=11)
    plt.tight_layout()
    cm_path = os.path.join(fig_dir, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300)
    plt.close()
    
    # 2. ROC Curve Plot
    try:
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        plt.figure(figsize=(6, 5))
        plt.plot(fpr, tpr, color='#1f77b4', lw=2.5, label=f'{model_name} (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle='--', label='Random Chance')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=11)
        plt.ylabel('True Positive Rate (Recall)', fontsize=11)
        plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=12, fontweight='bold', pad=12)
        plt.legend(loc='lower right', frameon=True)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        roc_path = os.path.join(fig_dir, 'roc_curve.png')
        plt.savefig(roc_path, dpi=300)
        plt.close()
    except Exception as e:
        print(f"Could not plot ROC curve: {e}")
        
    return metrics
