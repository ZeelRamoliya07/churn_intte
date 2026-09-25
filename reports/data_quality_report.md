# Data Quality Report: Telco Customer Churn Dataset

---

## 1. Reproducibility & Metadata

* **Dataset Filename:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`
* **Dataset Location:** `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`
* **Original Source:** IBM Sample Data Repository / Kaggle
* **Source URL:** [https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv](https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv)
* **Retrieval Date:** September 25, 2026
* **File Format:** CSV (Comma-Separated Values)
* **Number of Records (Rows):** 7,043
* **Number of Attributes (Columns):** 21

---

## 2. Dataset Dimensions & Schema

The dataset contains 7,043 rows and 21 columns representing customer account parameters, subscribed telecommunication services, billing information, and historical churn status.

* **Total Rows:** 7,043
* **Total Columns:** 21

---

## 3. Duplicate Records

* **Exact Duplicate Rows Count:** 0
* **Observation:** All 7,043 rows represent distinct customer records based on full-row comparison.

---

## 4. Missing-Value Summary

* **Standard `NaN` / `NULL` Count:** 0 across all 21 columns.
* **Implicit Missing Values (Whitespace Strings):** 11 records in column `TotalCharges`.
  * **Affected Column:** `TotalCharges`
  * **Implicit Missing Count:** 11
  * **Missing Percentage:** 0.156% (~0.16%)
  * **Observation:** The `TotalCharges` column contains string values where 11 entries consist solely of empty spaces (`" "`). All 11 records correspond to customers with `tenure == 0`, indicating newly enrolled customers who have not completed a full billing cycle.

---

## 5. Data-Type Summary

* **Categorical / Text Columns (`object`):** 18 columns (`customerID`, `gender`, `Partner`, `Dependents`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `TotalCharges`, `Churn`)
* **Numerical Columns (`int64`, `float64`):** 3 columns
  * `SeniorCitizen` (`int64` — binary 0/1 representation)
  * `tenure` (`int64` — integer months)
  * `MonthlyCharges` (`float64` — continuous monetary amount)

* **Data-Type Discrepancy Observation:** `TotalCharges` is stored as pandas `object` (string) rather than `float64` due to the 11 whitespace entries noted above.

---

## 6. Target Distribution (`Churn`)

* **Target Attribute Name:** `Churn`
* **Raw Target Encoding:** `"No"` (Retained), `"Yes"` (Churned)
* **Class Representation:**

| Target Class | Description | Raw Count | Percentage (%) |
| :--- | :--- | :--- | :--- |
| `"No"` | Retained Customer | 5,174 | 73.46% |
| `"Yes"` | Churned Customer | 1,869 | 26.54% |
| **Total** | | **7,043** | **100.00%** |

* **Class Balance Observation:** The dataset exhibits class imbalance, with retained customers outnumbering churned customers in a ratio of approximately 2.77 to 1 (73.5% vs. 26.5%).

---

## 7. Suspicious Values & Edge Cases

1. **Blank `TotalCharges` Entries (`" "`):**
   * Exactly 11 rows contain `" "` for `TotalCharges`.
   * All 11 instances have `tenure == 0` and `Churn == "No"`.
2. **Redundant Service Category Values:**
   * Columns `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, and `StreamingMovies` contain a 3rd distinct category: `"No internet service"`.
   * Column `MultipleLines` contains a 3rd distinct category: `"No phone service"`.
   * These sub-categories map directly to `InternetService == "No"` and `PhoneService == "No"`, respectively.

---

## 8. Potential Data-Quality Concerns

* **String Formatting in Numeric Columns:** Parsing `TotalCharges` to floating-point representation will require handling the 11 empty space values.
* **Class Imbalance:** Machine learning evaluation in future phases must account for the 73.5% / 26.5% target distribution (e.g., measuring F1-score, Recall, ROC-AUC rather than relying on accuracy alone).
* **Multi-Category Redundancies:** Service add-on features contain nested logical dependencies with primary service indicators (`InternetService` / `PhoneService`).

---

## 9. Potential Identifier Columns

* **`customerID`:** Contains 7,043 unique alphanumeric strings (e.g., `7590-VHVEG`).
* **Observation:** `customerID` serves as a primary record identifier and carries no generalizable domain predictive information.

---

## 10. Initial Summary Observations

* The raw dataset was successfully acquired and verified without applying data modifications, feature transformations, or model fitting.
* All 7,043 records were profiled across 21 columns.
* Data quality concerns are limited to 11 blank `TotalCharges` values and categorical text formats.
* The original CSV file in `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` remains strictly untouched.
