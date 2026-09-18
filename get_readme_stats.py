import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy import stats
import numpy as np

df_raw = pd.read_csv('data/indian_bank_customer_churn.csv')
df_clean = pd.read_csv('data/cleaned_indian_bank_churn.csv')

raw_rows = len(df_raw)
clean_rows = len(df_clean)

overall_churn = df_clean['Churn'].mean() * 100

df_clean['AgeGroup'] = np.where(df_clean['Age'] > 50, '>50', '<=50')
contingency = pd.crosstab(df_clean['AgeGroup'], df_clean['Churn'])
chi2, p_val, dof, ex = stats.chi2_contingency(contingency)

X = df_clean.drop(columns=['CustomerID', 'Churn', 'AgeGroup'])
y = df_clean['Churn']
cat_cols = ['Gender', 'Location']
num_cols = ['Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCreditCard', 'IsActiveMember', 'EstimatedSalary']
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_cols)
])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

lr = Pipeline([('preprocessor', preprocessor), ('classifier', LogisticRegression(random_state=42, max_iter=1000))])
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

rf = Pipeline([('preprocessor', preprocessor), ('classifier', RandomForestClassifier(random_state=42, n_estimators=100, class_weight='balanced'))])
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

stats_dict = {
    "raw_rows": raw_rows,
    "clean_rows": clean_rows,
    "overall_churn": round(overall_churn, 2),
    "p_val": p_val,
    "lr": {
        "acc": round(accuracy_score(y_test, y_pred_lr), 4),
        "f1": round(f1_score(y_test, y_pred_lr), 4)
    },
    "rf": {
        "acc": round(accuracy_score(y_test, y_pred_rf), 4),
        "f1": round(f1_score(y_test, y_pred_rf), 4)
    }
}
with open('outputs/stats.json', 'w') as f:
    json.dump(stats_dict, f)
print("Stats saved.")
