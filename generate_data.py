import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 10000

customer_ids = np.arange(10001, 10001 + n_samples)
genders = np.random.choice(['Male', 'Female', 'M', 'F'], n_samples, p=[0.48, 0.46, 0.03, 0.03])
locations = np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'DELHI', 'mumbai'], n_samples)
ages = np.random.normal(40, 12, n_samples).clip(18, 85)
tenure = np.random.randint(0, 11, n_samples)
balance = np.random.normal(65000, 25000, n_samples).clip(0, 150000)
num_of_products = np.random.choice([1, 2, 3, 4], n_samples, p=[0.50, 0.44, 0.04, 0.02])
has_crcard = np.random.choice([1, 0], n_samples, p=[0.70, 0.30])
is_active = np.random.choice([1, 0], n_samples, p=[0.52, 0.48])
estimated_salary = np.random.normal(85000, 35000, n_samples).clip(15000, 200000)

# Realistic Logistic Log-Odds formulation
logit = (
    -2.8
    + 0.045 * (ages - 40)
    + 0.85 * (1 - is_active)
    + 1.30 * (num_of_products >= 3)
    - 0.40 * (num_of_products == 2)
    + 0.000015 * (balance - 65000)
    - 0.08 * (tenure - 5)
    + np.random.normal(0, 0.4, n_samples)
)

churn_prob = 1 / (1 + np.exp(-logit))
churn = (np.random.rand(n_samples) < churn_prob).astype(int)

df = pd.DataFrame({
    'CustomerID': customer_ids,
    'Gender': genders,
    'Location': locations,
    'Age': np.round(ages, 1),
    'Tenure': tenure,
    'Balance': balance,
    'NumOfProducts': num_of_products,
    'HasCreditCard': has_crcard,
    'IsActiveMember': is_active,
    'EstimatedSalary': np.round(estimated_salary, 2),
    'Churn': churn
})

# Inject real-world dirty data anomalies for data cleaning demonstration
# Missing values
df.loc[np.random.choice(df.index, 142, replace=False), 'Age'] = np.nan
df.loc[np.random.choice(df.index, 195, replace=False), 'EstimatedSalary'] = np.nan

# Datatype issues (Balance as string with rupees)
df['Balance'] = df['Balance'].apply(lambda x: f"₹ {x:,.2f}" if not pd.isna(x) else x)

# Add duplicate records
duplicates = df.sample(50, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

df.to_csv('data/indian_bank_customer_churn.csv', index=False)
print(f"Dataset generated: {len(df)} rows. Base Churn Rate: {df['Churn'].mean():.2%}")
