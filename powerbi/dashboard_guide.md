# Customer Churn Power BI Dashboard Guide

This guide will walk you through creating a stunning, interactive Power BI dashboard using the exported data (`powerbi_export.csv`).

## 1. Import Data
1. Open Power BI Desktop.
2. Click **Get Data** -> **Text/CSV**.
3. Select `powerbi_export.csv` from the `powerbi/` folder in this repository.
4. Click **Load**. (The data is already cleaned and pre-processed by our Python scripts).

## 2. Dashboard Layout & Theme
To achieve a premium, modern aesthetic:
- **Theme**: Go to *View* -> *Themes* -> *Customize current theme*. Use a sleek dark mode palette (e.g., Background: `#1E1E1E`, Text: `#FFFFFF`, Primary Color: `#00E5FF` (Cyan) for non-churn, `#FF3D71` (Pink/Red) for churn).
- **Background**: Add a subtle dark gradient or use rounded rectangles (Shapes) behind your charts to create a "glassmorphism" or card effect.

## 3. Key Visualizations

### A. Top Level KPIs (Cards)
Use the **Card** visual for these high-level metrics, placed at the top of your dashboard.
1. **Total Customers**: Count of `CustomerID` (or row count).
2. **Overall Churn Rate**: 
   - *DAX Measure*: `Churn Rate = SUM('powerbi_export'[Actual_Churn]) / COUNTROWS('powerbi_export')`
   - Format as Percentage.
3. **Average Predicted Probability**: 
   - Average of `Predicted_Churn_Prob`.

### B. Churn by Demographic Segments (Donut/Pie Charts)
1. **Churn by Gender**:
   - Visual: Donut Chart
   - Legend: `Gender`
   - Values: Count of Customers
   - Filter (Visual Level): `Actual_Churn = 1`
2. **Churn by Location**:
   - Visual: Map or Bar Chart
   - Axis/Location: `Location`
   - Values: `Churn Rate` (DAX Measure)

### C. Trend over Time (Tenure)
1. **Churn Rate over Tenure**:
   - Visual: Line Chart
   - X-Axis: `Tenure`
   - Y-Axis: `Churn Rate` (DAX Measure)
   - Formatting: Smooth line, add markers.

### D. At-Risk Customer Segments
1. **High-Risk Profiles (Matrix/Table)**:
   - Visual: Matrix
   - Rows: `NumOfProducts`, `IsActiveMember`
   - Values: `Churn Rate`, `Count of Customers`
   - *Conditional Formatting*: Apply background color gradient to the Churn Rate column (Red for high).

### E. Model Performance (Scatter/Bar)
1. **Actual vs Predicted**:
   - Visual: 100% Stacked Bar Chart
   - Axis: `Predicted_Churn`
   - Legend: `Actual_Churn`
   - This shows the model's accuracy visually (how many predicted churns actually churned).

## 4. Interactivity (Slicers)
Add **Slicers** on the left panel or top right to allow users to drill down:
- `Location`
- `Gender`
- `HasCreditCard`
- `IsActiveMember`

*Tip: Change slicer settings to "Dropdown" or "Tile" for a cleaner look.*

## 5. Polish
- Remove gridlines on charts to reduce clutter.
- Ensure all titles are clean and readable (e.g., "Churn Rate by Tenure" instead of "Average of Actual_Churn by Tenure").
- Add tooltips to visuals so hovering reveals the exact customer counts and percentages.
