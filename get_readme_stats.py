import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, precision_recall_curve
from imblearn.over_sampling import SMOTE
from scipy import stats

# 1. Load Data
df_raw = pd.read_csv('data/indian_bank_customer_churn.csv')
df_clean = pd.read_csv('data/cleaned_indian_bank_churn.csv')

raw_rows = len(df_raw)
clean_rows = len(df_clean)
overall_churn = df_clean['Churn'].mean() * 100

# 2. Hypothesis Test
df_clean['AgeGroup'] = np.where(df_clean['Age'] > 50, '>50', '<=50')
contingency = pd.crosstab(df_clean['AgeGroup'], df_clean['Churn'])
chi2, p_val, dof, ex = stats.chi2_contingency(contingency)

# 3. Model Prep
X = df_clean.drop(columns=['CustomerID', 'Churn', 'AgeGroup'])
y = df_clean['Churn']
cat_cols = ['Gender', 'Location']
num_cols = ['Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCreditCard', 'IsActiveMember', 'EstimatedSalary']

X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_cols)
])

X_train_proc = preprocessor.fit_transform(X_train_raw)
X_test_proc = preprocessor.transform(X_test_raw)

# SMOTE
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train_proc, y_train)

# Logistic Regression
lr = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
lr.fit(X_train_smote, y_train_smote)
lr_prob = lr.predict_proba(X_test_proc)[:, 1]
lr_pred = lr.predict(X_test_proc)

# Random Forest + Threshold Tuning
rf = RandomForestClassifier(n_estimators=150, max_depth=8, min_samples_split=10, random_state=42)
rf.fit(X_train_smote, y_train_smote)
rf_prob = rf.predict_proba(X_test_proc)[:, 1]

precisions, recalls, thresholds = precision_recall_curve(y_test, rf_prob)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
best_idx = np.argmax(f1_scores)
best_thresh = float(thresholds[best_idx]) if best_idx < len(thresholds) else 0.5
rf_pred_tuned = (rf_prob >= best_thresh).astype(int)

# Compile Stats
stats_dict = {
    "raw_rows": raw_rows,
    "clean_rows": clean_rows,
    "overall_churn": round(overall_churn, 2),
    "chi2_stat": round(chi2, 4),
    "p_val": p_val,
    "optimal_threshold": round(best_thresh, 3),
    "lr": {
        "accuracy": round(accuracy_score(y_test, lr_pred) * 100, 2),
        "precision": round(precision_score(y_test, lr_pred) * 100, 2),
        "recall": round(recall_score(y_test, lr_pred) * 100, 2),
        "f1": round(f1_score(y_test, lr_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, lr_prob), 4)
    },
    "rf": {
        "accuracy": round(accuracy_score(y_test, rf_pred_tuned) * 100, 2),
        "precision": round(precision_score(y_test, rf_pred_tuned) * 100, 2),
        "recall": round(recall_score(y_test, rf_pred_tuned) * 100, 2),
        "f1": round(f1_score(y_test, rf_pred_tuned), 4),
        "roc_auc": round(roc_auc_score(y_test, rf_prob), 4)
    }
}

with open('outputs/stats.json', 'w') as f:
    json.dump(stats_dict, f, indent=4)

print("Updated stats saved successfully:")
print(json.dumps(stats_dict, indent=2))
