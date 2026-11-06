"""
Generate Fig 6: Database / Dataset Schema for Water Potability Project
Author: URLA ENOCH PHILIP (23ME1A54B1)
Guide: Mr. E. Surendra babu
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig_dir = r'C:\Users\RATNAM\.gemini\antigravity\scratch\water-potability-svm\reports\figures'
os.makedirs(fig_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5.0, 9.6, 'Dataset & Pipeline Entity Schema — Water Potability System', 
        ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')

# Table 1: Raw Water Quality Records (water_potability.csv)
box1 = patches.FancyBboxPatch((0.5, 5.0), 4.2, 4.0, boxstyle="square,pad=0.1", fc='#eff6ff', ec='#1d4ed8', lw=1.5)
ax.add_patch(box1)
header1 = patches.Rectangle((0.5, 8.4), 4.2, 0.6, fc='#1d4ed8')
ax.add_patch(header1)
ax.text(2.6, 8.7, "water_potability.csv (Raw Records)", ha='center', va='center', fontsize=9, fontweight='bold', color='white')
t1_text = (
    "• ph : float (0.0 - 14.0)\n"
    "• Hardness : float (mg/L)\n"
    "• Solids : float (ppm - TDS)\n"
    "• Chloramines : float (ppm)\n"
    "• Sulfate : float (mg/L)\n"
    "• Conductivity : float (uS/cm)\n"
    "• Organic_carbon : float (ppm)\n"
    "• Trihalomethanes : float (ug/L)\n"
    "• Turbidity : float (NTU)\n"
    "• Potability : int [Target: 0 or 1]"
)
ax.text(0.7, 6.7, t1_text, fontsize=7.5, va='center', color='#1e293b', fontfamily='monospace')

# Table 2: Preprocessed Matrix
box2 = patches.FancyBboxPatch((5.3, 5.4), 4.2, 3.6, boxstyle="square,pad=0.1", fc='#f0fdf4', ec='#15803d', lw=1.5)
ax.add_patch(box2)
header2 = patches.Rectangle((5.3, 8.4), 4.2, 0.6, fc='#15803d')
ax.add_patch(header2)
ax.text(7.4, 8.7, "Preprocessed Feature Matrix", ha='center', va='center', fontsize=9, fontweight='bold', color='white')
t2_text = (
    "• X_train_scaled : ndarray (2620, 9)\n"
    "• X_test_scaled  : ndarray (656, 9)\n"
    "• y_train        : ndarray (2620,)\n"
    "• y_test         : ndarray (656,)\n"
    "• imputer.pkl    : SimpleImputer\n"
    "• scaler.pkl     : StandardScaler"
)
ax.text(5.5, 6.9, t2_text, fontsize=7.5, va='center', color='#14532d', fontfamily='monospace')

# Table 3: Serialized SVM Model
box3 = patches.FancyBboxPatch((0.5, 0.8), 4.2, 3.4, boxstyle="square,pad=0.1", fc='#faf5ff', ec='#7e22ce', lw=1.5)
ax.add_patch(box3)
header3 = patches.Rectangle((0.5, 3.6), 4.2, 0.6, fc='#7e22ce')
ax.add_patch(header3)
ax.text(2.6, 3.9, "Trained SVM Model (Artifacts)", ha='center', va='center', fontsize=9, fontweight='bold', color='white')
t3_text = (
    "• Kernel : RBF (Radial Basis Function)\n"
    "• Hyperparameters : C=3.0, gamma=0.1\n"
    "• Class Weight : balanced\n"
    "• Test Accuracy : 88.57%\n"
    "• Test Recall : 90.53%\n"
    "• Test ROC-AUC : 0.9603"
)
ax.text(0.7, 2.2, t3_text, fontsize=7.5, va='center', color='#581c87', fontfamily='monospace')

# Table 4: Public Health Surveillance Output
box4 = patches.FancyBboxPatch((5.3, 0.8), 4.2, 3.4, boxstyle="square,pad=0.1", fc='#fff1f2', ec='#be123c', lw=1.5)
ax.add_patch(box4)
header4 = patches.Rectangle((5.3, 3.6), 4.2, 0.6, fc='#be123c')
ax.add_patch(header4)
ax.text(7.4, 3.9, "Surveillance Output Schema", ha='center', va='center', fontsize=9, fontweight='bold', color='white')
t4_text = (
    "• Predicted_Class : 'Potable' / 'Hazard'\n"
    "• Confidence_Prob : float (0.0% - 100%)\n"
    "• WHO_Violations : list[str]\n"
    "• Filtration_Advice : str\n"
    "• Mineral_Advice : str\n"
    "• Chemical_Advice : str"
)
ax.text(5.5, 2.2, t4_text, fontsize=7.5, va='center', color='#881337', fontfamily='monospace')

# Connectors
ax.annotate("", xy=(5.3, 7.0), xytext=(4.7, 7.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1e293b'))
ax.text(5.0, 7.2, "impute &\nscale", ha='center', va='bottom', fontsize=7)

ax.annotate("", xy=(2.6, 4.2), xytext=(2.6, 5.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1e293b'))
ax.text(2.6, 4.6, "train &\nfit", ha='right', va='center', fontsize=7)

ax.annotate("", xy=(5.3, 2.5), xytext=(4.7, 2.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1e293b'))
ax.text(5.0, 2.7, "predict &\nadvise", ha='center', va='bottom', fontsize=7)

ax.text(5.0, 0.2, "Fig. 6: Dataset and System Entity Schema", ha='center', va='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig6_dataset_schema.png'), bbox_inches='tight')
plt.close()
print("fig6_dataset_schema.png generated successfully!")
