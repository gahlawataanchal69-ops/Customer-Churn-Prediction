-- schema.sql
-- Create the cleaned table structure for SQLite

DROP TABLE IF EXISTS customer_churn;

CREATE TABLE customer_churn (
    CustomerID INTEGER PRIMARY KEY,
    Gender TEXT,
    Location TEXT,
    Age REAL,
    Tenure INTEGER,
    Balance REAL,
    NumOfProducts INTEGER,
    HasCreditCard INTEGER,
    IsActiveMember INTEGER,
    EstimatedSalary REAL,
    Churn INTEGER
);
