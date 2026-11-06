"""
Generate Project Report Architecture & Flow Diagrams for B.Tech Documentation
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

def create_fig1_architecture():
    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.6, 'System Architecture — Water Potability Classification', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # Layers
    layers = [
        ("Presentation Layer (Streamlit UI)", 8.2, '#eff6ff', '#3b82f6', 
         "Interactive Web Console | Physical-Chemical Sliders | Real-Time Health Badge | Surveillance Log"),
        ("Ingestion & Validation Layer", 6.4, '#f0fdf4', '#22c55e', 
         "Municipal CSV Ingestion | Single-Sample Dict Parser | Pydantic Schema Validation"),
        ("Preprocessing & Transformation Layer", 4.6, '#fefce8', '#eab308', 
         "SimpleImputer (Median Imputation) | StandardScaler (Zero Mean, Unit Variance Normalization)"),
        ("Machine Learning AI Layer (SVM)", 2.8, '#faf5ff', '#a855f7', 
         "Optimal RBF Kernel SVC (C=3.0, gamma=0.1) | Decision Function & Probability Calibrator"),
        ("Advisory & Surveillance Output Layer", 1.0, '#fff1f2', '#f43f5e', 
         "Potability Categorization | WHO Safety Compliance | Public-Health Interventions & Report Export")
    ]

    for title, y, facecolor, edgecolor, desc in layers:
        rect = patches.FancyBboxPatch((0.8, y-0.6), 8.4, 1.1,
                                     boxstyle="round,pad=0.2",
                                     fc=facecolor, ec=edgecolor, lw=1.8)
        ax.add_patch(rect)
        ax.text(5, y+0.25, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1e293b')
        ax.text(5, y-0.15, desc, ha='center', va='center', fontsize=8.5, color='#475569')

        if y > 1.5:
            ax.annotate('', xy=(5, y-0.6), xytext=(5, y-0.85),
                        arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.8))

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig1_system_architecture.png'), bbox_inches='tight')
    plt.close()

def create_fig2_dfd_level0():
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Entity 1: User / Health Officer
    e1 = patches.FancyBboxPatch((0.5, 2.2), 2.2, 1.6, boxstyle="square,pad=0.1", fc='#f8fafc', ec='#1e293b', lw=1.5)
    ax.add_patch(e1)
    ax.text(1.6, 3.0, "Municipal Officer /\nHealth Analyst", ha='center', va='center', fontsize=9.5, fontweight='bold')

    # Central Process: 0 Water Potability Classification System
    circle = patches.Circle((5.0, 3.0), 1.2, fc='#eff6ff', ec='#2563eb', lw=2)
    ax.add_patch(circle)
    ax.text(5.0, 3.2, "0", ha='center', va='center', fontsize=12, fontweight='bold', color='#1d4ed8')
    ax.text(5.0, 2.8, "Water Potability\nClassification System", ha='center', va='center', fontsize=9, fontweight='bold')

    # Entity 2: WHO Standards Knowledgebase
    e2 = patches.FancyBboxPatch((7.3, 2.2), 2.2, 1.6, boxstyle="square,pad=0.1", fc='#f8fafc', ec='#1e293b', lw=1.5)
    ax.add_patch(e2)
    ax.text(8.4, 3.0, "WHO Standards &\nIntervention Rules", ha='center', va='center', fontsize=9.5, fontweight='bold')

    # Arrows
    ax.annotate("Water Test Parameters / CSV", xy=(3.8, 3.4), xytext=(2.7, 3.4),
                arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.4), fontsize=8, ha='center', va='bottom')
    ax.annotate("Diagnostic Report & Advice", xy=(2.7, 2.6), xytext=(3.8, 2.6),
                arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.4), fontsize=8, ha='center', va='top')
    ax.annotate("Permissible Thresholds", xy=(6.2, 3.0), xytext=(7.3, 3.0),
                arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.4), fontsize=8, ha='center', va='bottom')

    ax.text(5.0, 0.4, "Fig. 2: Data Flow Diagram – Level 0", ha='center', va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig2_dfd_level0.png'), bbox_inches='tight')
    plt.close()

def create_fig3_dfd_level1():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Processes
    procs = [
        ("1.0 Ingest & Validate", 2.2, 6.2),
        ("2.0 Impute & Scale", 6.8, 6.2),
        ("3.0 SVM Potability Predict", 6.8, 2.5),
        ("4.0 Advisory Generation", 2.2, 2.5)
    ]
    for name, x, y in procs:
        c = patches.Circle((x, y), 0.9, fc='#eff6ff', ec='#2563eb', lw=1.8)
        ax.add_patch(c)
        ax.text(x, y, name.replace(" ", "\n"), ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Data Stores
    d1 = patches.FancyBboxPatch((4.0, 4.2), 2.0, 0.8, boxstyle="square,pad=0.05", fc='#fefce8', ec='#ca8a04', lw=1.5)
    ax.add_patch(d1)
    ax.text(5.0, 4.6, "D1: Pretrained Model\n& Scaler Artifacts", ha='center', va='center', fontsize=8, fontweight='bold')

    # Arrows between processes
    ax.annotate("Raw Sample / CSV", xy=(1.3, 6.2), xytext=(0.2, 6.2),
                arrowprops=dict(arrowstyle="->", lw=1.3), fontsize=7.5, va='bottom')
    ax.annotate("Validated Data", xy=(5.9, 6.2), xytext=(3.1, 6.2),
                arrowprops=dict(arrowstyle="->", lw=1.3), fontsize=7.5, va='bottom')
    ax.annotate("Standardized Vectors", xy=(6.8, 3.4), xytext=(6.8, 5.3),
                arrowprops=dict(arrowstyle="->", lw=1.3), fontsize=7.5, ha='left')
    ax.annotate("Prediction + Probability", xy=(3.1, 2.5), xytext=(5.9, 2.5),
                arrowprops=dict(arrowstyle="->", lw=1.3), fontsize=7.5, va='bottom')
    ax.annotate("Final Dashboard Display", xy=(0.2, 2.5), xytext=(1.3, 2.5),
                arrowprops=dict(arrowstyle="<-", lw=1.3), fontsize=7.5, va='bottom')
    
    # D1 to 2.0 and 3.0
    ax.annotate("", xy=(6.3, 5.7), xytext=(5.5, 5.0), arrowprops=dict(arrowstyle="->", lw=1.2, ls="--"))
    ax.annotate("", xy=(6.3, 3.1), xytext=(5.5, 4.2), arrowprops=dict(arrowstyle="->", lw=1.2, ls="--"))

    ax.text(5.0, 0.5, "Fig. 3: Data Flow Diagram – Level 1", ha='center', va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig3_dfd_level1.png'), bbox_inches='tight')
    plt.close()

def create_fig4_usecase():
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Actor Head & Body
    head = patches.Circle((1.2, 5.8), 0.35, fc='#334155', ec='#0f172a', lw=1.5)
    ax.add_patch(head)
    ax.plot([1.2, 1.2], [5.45, 4.6], color='#0f172a', lw=2) # body
    ax.plot([0.8, 1.6], [5.1, 5.1], color='#0f172a', lw=2) # arms
    ax.plot([1.2, 0.8], [4.6, 4.0], color='#0f172a', lw=2) # leg left
    ax.plot([1.2, 1.6], [4.6, 4.0], color='#0f172a', lw=2) # leg right
    ax.text(1.2, 3.5, "User / Public\nHealth Official", ha='center', va='center', fontsize=9.5, fontweight='bold')

    # System Boundary Box
    rect = patches.FancyBboxPatch((3.0, 0.8), 6.5, 8.4, boxstyle="round,pad=0.2", fc='#f8fafc', ec='#64748b', lw=1.5)
    ax.add_patch(rect)
    ax.text(6.25, 8.8, "Water Potability Monitoring System", ha='center', va='center', fontsize=10, fontweight='bold', color='#1e3a8a')

    use_cases = [
        ("Input Physical-Chemical Readings", 7.8),
        ("Select Quick Preset Scenarios", 6.6),
        ("Perform Single Sample SVM Diagnosis", 5.4),
        ("Upload Municipal Batch Test CSV", 4.2),
        ("Inspect WHO Compliance & Health Advice", 3.0),
        ("Analyze SVM Performance & ROC Curves", 1.8)
    ]

    for uc_text, y in use_cases:
        e = patches.Ellipse((6.25, y), 5.2, 0.8, fc='#eff6ff', ec='#2563eb', lw=1.3)
        ax.add_patch(e)
        ax.text(6.25, y, uc_text, ha='center', va='center', fontsize=8.5, fontweight='bold')
        ax.plot([1.8, 3.65], [5.0, y], color='#94a3b8', lw=1.1)

    ax.text(5.0, 0.2, "Fig. 4: Use Case Diagram", ha='center', va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig4_use_case_diagram.png'), bbox_inches='tight')
    plt.close()

def create_fig5_sequence():
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    lifelines = [
        ("User", 1.2),
        ("Streamlit UI", 3.4),
        ("Preprocessor", 5.6),
        ("SVM Model", 7.6),
        ("Advisory Engine", 9.2)
    ]

    for name, x in lifelines:
        box = patches.FancyBboxPatch((x-0.8, 9.0), 1.6, 0.6, boxstyle="square,pad=0.1", fc='#e2e8f0', ec='#1e293b', lw=1.2)
        ax.add_patch(box)
        ax.text(x, 9.3, name, ha='center', va='center', fontsize=8.5, fontweight='bold')
        ax.plot([x, x], [8.9, 0.8], color='#cbd5e1', lw=1.2, ls='--')

    messages = [
        (8.2, 1.2, 3.4, "1. Enter water parameters"),
        (7.4, 3.4, 5.6, "2. transform_sample(data)"),
        (6.6, 5.6, 5.6, "3. Impute nulls & Scale features"),
        (5.8, 5.6, 7.6, "4. model.predict_proba(X_scaled)"),
        (5.0, 7.6, 3.4, "5. Return potability label & prob"),
        (4.2, 3.4, 9.2, "6. Check WHO guidelines(sample)"),
        (3.4, 9.2, 3.4, "7. Return actionable interventions"),
        (2.6, 3.4, 1.2, "8. Render health badge & advice")
    ]

    for y, x1, x2, msg in messages:
        if x1 == x2: # Self call
            ax.annotate('', xy=(x1, y-0.3), xytext=(x1+0.6, y-0.1),
                        arrowprops=dict(arrowstyle="->", color='#2563eb', lw=1.2))
            ax.plot([x1, x1+0.6, x1+0.6], [y, y, y-0.1], color='#2563eb', lw=1.2)
            ax.text(x1+0.7, y-0.15, msg, fontsize=7.5, va='center')
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color='#2563eb' if x1<x2 else '#10b981', lw=1.2))
            ax.text((x1+x2)/2, y+0.15, msg, ha='center', va='bottom', fontsize=7.5)

    ax.text(5.0, 0.2, "Fig. 5: Sequence Diagram", ha='center', va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig5_sequence_diagram.png'), bbox_inches='tight')
    plt.close()

def create_fig7_module_interaction():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    mods = [
        ("Module 1:\nData Ingestion &\nValidation", 1.2, 3.0),
        ("Module 2:\nMedian Imputation &\nScaling Pipeline", 3.8, 3.0),
        ("Module 3:\nSupport Vector\nMachine Classifier", 6.4, 3.0),
        ("Module 4:\nPublic Health\nAdvisory Engine", 8.8, 3.0)
    ]

    for name, x, y in mods:
        r = patches.FancyBboxPatch((x-1.0, y-0.9), 2.0, 1.8, boxstyle="round,pad=0.15", fc='#eff6ff', ec='#2563eb', lw=1.6)
        ax.add_patch(r)
        ax.text(x, y, name, ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Flow arrows
    ax.annotate("Raw Records", xy=(2.8, 3.0), xytext=(2.2, 3.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("Scaled Matrix", xy=(5.4, 3.0), xytext=(4.8, 3.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("Potability & P(y=1)", xy=(7.8, 3.0), xytext=(7.4, 3.0), arrowprops=dict(arrowstyle="->", lw=1.5))

    # Module 5 wrapper on top
    r5 = patches.FancyBboxPatch((1.0, 0.8), 8.0, 1.2, boxstyle="round,pad=0.15", fc='#f0fdf4', ec='#16a34a', lw=1.6)
    ax.add_patch(r5)
    ax.text(5.0, 1.4, "Module 5: Streamlit Interactive Web Application & Surveillance Console", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#14532d')

    ax.annotate("", xy=(5.0, 2.1), xytext=(5.0, 1.8), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#16a34a'))

    ax.text(5.0, 0.2, "Fig. 7: Module Interaction Flow", ha='center', va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig7_module_interaction.png'), bbox_inches='tight')
    plt.close()

def create_fig8_flow():
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    ax.axis('off')

    steps = [
        ("Raw Water Quality Dataset (3,276 records)", 8.2, '#f8fafc', '#1e293b'),
        ("Stratified 80/20 Partitioning (Train/Test)", 7.0, '#eff6ff', '#2563eb'),
        ("Missing Value Median Imputation (ph, Sulfate, Trihalomethanes)", 5.8, '#eff6ff', '#2563eb'),
        ("StandardScaler Distance Normalization (Zero Mean, Unit Std)", 4.6, '#eff6ff', '#2563eb'),
        ("GridSearchCV 3-Fold Stratified Tuning (C=3.0, gamma=0.1, RBF)", 3.4, '#faf5ff', '#a855f7'),
        ("Model Evaluation: 88.57% Acc, 90.53% Recall, 0.9603 ROC-AUC", 2.2, '#f0fdf4', '#16a34a'),
        ("Artifact Serialization (water_potability_svm_model.pkl)", 1.0, '#fff1f2', '#e11d48')
    ]

    for text, y, fc, ec in steps:
        r = patches.FancyBboxPatch((1.0, y-0.4), 8.0, 0.8, boxstyle="round,pad=0.1", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(r)
        ax.text(5.0, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold')
        if y > 1.2:
            ax.annotate('', xy=(5.0, y-0.4), xytext=(5.0, y-0.6), arrowprops=dict(arrowstyle="->", lw=1.4, color='#475569'))

    ax.text(5.0, 0.2, "Fig. 8: Model Training, Tuning and Serialization Workflow", ha='center', va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig8_training_optimization_flow.png'), bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_fig1_architecture()
    create_fig2_dfd_level0()
    create_fig3_dfd_level1()
    create_fig4_usecase()
    create_fig5_sequence()
    create_fig7_module_interaction()
    create_fig8_flow()
    print("All architecture and workflow diagrams generated successfully!")
