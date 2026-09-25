# Data Dictionary: Telco Customer Churn Dataset

This document details all 21 columns in the raw IBM Telco Customer Churn dataset (`WA_Fn-UseC_-Telco-Customer-Churn.csv`).

---

## Dataset Overview

* **Dataset Name:** Telco Customer Churn Dataset
* **Source:** IBM Community / Kaggle
* **Source URL:** [https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv](https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv)
* **License:** Public Domain / Open Dataset (IBM Sample Data)
* **Dimensions:** 7,043 rows, 21 columns
* **Target Variable:** `Churn`

---

## Detailed Column Specifications

| Column Name | Raw Dtype | Logical Type | Role | Example Values | Description / Meaning | Missing Count (%) | Unique Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `customerID` | `object` | Categorical | Identifier | `7590-VHVEG`, `5575-GNVDE` | Unique alpha-numeric customer account identifier | 0 (0.00%) | 7,043 |
| `gender` | `object` | Categorical | Feature | `Female`, `Male` | Customer gender identity | 0 (0.00%) | 2 |
| `SeniorCitizen` | `int64` | Categorical (Binary) | Feature | `0`, `1` | Indicates if customer is a senior citizen (1) or not (0) | 0 (0.00%) | 2 |
| `Partner` | `object` | Categorical | Feature | `Yes`, `No` | Indicates if customer has a partner | 0 (0.00%) | 2 |
| `Dependents` | `object` | Categorical | Feature | `No`, `Yes` | Indicates if customer has dependents | 0 (0.00%) | 2 |
| `tenure` | `int64` | Numerical (Integer) | Feature | `1`, `34`, `72` | Number of months the customer has stayed with the company | 0 (0.00%) | 73 |
| `PhoneService` | `object` | Categorical | Feature | `Yes`, `No` | Indicates if customer has a phone service subscription | 0 (0.00%) | 2 |
| `MultipleLines` | `object` | Categorical | Feature | `No`, `Yes`, `No phone service` | Indicates if customer has multiple phone lines | 0 (0.00%) | 3 |
| `InternetService` | `object` | Categorical | Feature | `DSL`, `Fiber optic`, `No` | Customer internet service provider type | 0 (0.00%) | 3 |
| `OnlineSecurity` | `object` | Categorical | Feature | `No`, `Yes`, `No internet service` | Indicates if customer has online security add-on | 0 (0.00%) | 3 |
| `OnlineBackup` | `object` | Categorical | Feature | `Yes`, `No`, `No internet service` | Indicates if customer has online backup add-on | 0 (0.00%) | 3 |
| `DeviceProtection` | `object` | Categorical | Feature | `No`, `Yes`, `No internet service` | Indicates if customer has device protection plan | 0 (0.00%) | 3 |
| `TechSupport` | `object` | Categorical | Feature | `No`, `Yes`, `No internet service` | Indicates if customer has tech support plan | 0 (0.00%) | 3 |
| `StreamingTV` | `object` | Categorical | Feature | `No`, `Yes`, `No internet service` | Indicates if customer streams TV programming | 0 (0.00%) | 3 |
| `StreamingMovies` | `object` | Categorical | Feature | `No`, `Yes`, `No internet service` | Indicates if customer streams movies | 0 (0.00%) | 3 |
| `Contract` | `object` | Categorical | Feature | `Month-to-month`, `One year`, `Two year` | Customer contract terms | 0 (0.00%) | 3 |
| `PaperlessBilling` | `object` | Categorical | Feature | `Yes`, `No` | Indicates if customer uses paperless billing | 0 (0.00%) | 2 |
| `PaymentMethod` | `object` | Categorical | Feature | `Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)` | Payment method used by customer | 0 (0.00%) | 4 |
| `MonthlyCharges` | `float64` | Numerical (Continuous) | Feature | `29.85`, `56.95`, `118.75` | Amount charged to customer monthly | 0 (0.00%) | 1,585 |
| `TotalCharges` | `object`* | Numerical (Continuous) | Feature | `29.85`, `1889.5`, `" "` | Total amount charged to customer over tenure | 11 (0.16%)** | 6,531 |
| `Churn` | `object` | Categorical (Binary) | Target | `No`, `Yes` | Indicates if customer churned within last month | 0 (0.00%) | 2 |

*\* Note on `TotalCharges`: Stored as raw pandas `object` due to 11 empty whitespace strings (`" "`).*  
*\*\* Note on Missing Values: The 11 whitespace values in `TotalCharges` represent implicit missing data for customers with `tenure == 0`.*

---

## Target Variable Summary (`Churn`)

* **Target Column:** `Churn`
* **Raw Values:** `"No"`, `"Yes"`
* **Raw Counts:**
  * `"No"` (Retained): 5,174 (73.46%)
  * `"Yes"` (Churned): 1,869 (26.54%)
* **Planned Standardized Encoding (Future Phases):**
  * `0` = Retained (`"No"`)
  * `1` = Churned (`"Yes"`)
  *(Note: The raw CSV file remains unmodified in `data/raw/`)*
