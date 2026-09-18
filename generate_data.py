import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 10000

# 1. Base Data
customer_ids = np.arange(10001, 10001 + n_samples)
genders = np.random.choice(['Male', 'Female', 'M', 'F'], n_samples, p=[0.5, 0.45, 0.03, 0.02])
locations = np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'DELHI', 'mumbai'], n_samples)
ages = np.random.normal(45, 15, n_samples)
ages = np.where(ages < 18, 18, ages)
ages = np.where(ages > 90, 90, ages)

tenure = np.random.randint(0, 11, n_samples)
balance = np.random.normal(50000, 30000, n_samples)
balance = np.where(balance < 0, 0, balance)
num_of_products = np.random.choice([1, 2, 3, 4], n_samples, p=[0.5, 0.45, 0.04, 0.01])
has_crcard = np.random.choice([1, 0], n_samples, p=[0.7, 0.3])
is_active = np.random.choice([1, 0], n_samples, p=[0.5, 0.5])
estimated_salary = np.random.normal(80000, 40000, n_samples)
estimated_salary = np.where(estimated_salary < 10000, 10000, estimated_salary)

# Generate Churn based on some logic (higher for high balance, low active, many products, high age)
churn_prob = (
    0.05 + 
    (ages > 50) * 0.10 + 
    (balance > 80000) * 0.05 + 
    (is_active == 0) * 0.15 + 
    (num_of_products >= 3) * 0.40 - 
    (tenure > 5) * 0.05
)
churn_prob = np.clip(churn_prob, 0, 1)
churn = np.random.binomial(1, churn_prob)

# Create DataFrame
df = pd.DataFrame({
    'CustomerID': customer_ids,
    'Gender': genders,
    'Location': locations,
    'Age': ages,
    'Tenure': tenure,
    'Balance': balance,
    'NumOfProducts': num_of_products,
    'HasCreditCard': has_crcard,
    'IsActiveMember': is_active,
    'EstimatedSalary': estimated_salary,
    'Churn': churn
})

# 2. Inject anomalies
# Missing values in Age and EstimatedSalary
df.loc[np.random.choice(df.index, 150, replace=False), 'Age'] = np.nan
df.loc[np.random.choice(df.index, 200, replace=False), 'EstimatedSalary'] = np.nan

# Datatype issues (Balance as string with rupees)
df['Balance'] = df['Balance'].apply(lambda x: f"₹ {x:,.2f}" if not pd.isna(x) else x)

# Add some duplicates
duplicates = df.sample(50, random_state=1)
df = pd.concat([df, duplicates], ignore_index=True)

# Save to CSV
df.to_csv('data/indian_bank_customer_churn.csv', index=False)
print(f"Dataset generated successfully with {len(df)} rows.")
