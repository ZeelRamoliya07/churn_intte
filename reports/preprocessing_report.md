# Data Preprocessing Report: Telco Customer Churn

**Project:** Customer Churn Prediction & Business Intelligence System  
**Phase:** Phase 4 — Data Preprocessing & Feature Engineering  
**Dataset:** IBM Telco Customer Churn (`WA_Fn-UseC_-Telco-Customer-Churn.csv`)  
**Date:** September 29, 2026  

---

## 1. Objective

The objective of Phase 4 is to design, implement, and validate a modular, leak-free preprocessing pipeline using scikit-learn. The pipeline transforms the raw Telco customer dataset into preprocessed feature matrices ready for machine learning model training (Phase 5–8) and real-time FastAPI REST API inference (Phase 11).

---

## 2. Raw Data Issues Addressed

1. **`TotalCharges` String Formatting:** The raw dataset stores `TotalCharges` as text (`object` dtype) containing 11 empty space entries (`" "`).
   * **Resolution:** Stripped whitespace and converted string entries to floating-point numbers (`float64`), explicitly coercing the 11 blank strings to `NaN`.
2. **Identifier Isolation:** The `customerID` attribute consists of 7,043 unique alphanumeric strings.
   * **Resolution:** Excluded `customerID` from input feature matrix `X` to prevent arbitrary identifier memorization.
3. **Target Text Representation:** Raw target values are stored as text (`"No"` and `"Yes"`).
   * **Resolution:** Mapped `"No"` $\rightarrow$ `0` and `"Yes"` $\rightarrow$ `1`.

---

## 3. Target Transformation

* **Raw Target Attribute:** `Churn`
* **Raw Target Encoding:** `"No"` / `"Yes"`
* **Standardized Target Representation:** `0` (Retained) / `1` (Churned)
* **Target Distribution Post-Processing:**
  * Class `0` (Retained): 5,174 records (**73.46%**)
  * Class `1` (Churned): 1,869 records (**26.54%**)

---

## 4. Identifier Handling

* **Attribute Name:** `customerID`
* **Handling Strategy:** Removed from feature matrix `X`.
* **Rationale:** `customerID` contains unique string identifiers per account (7,043 unique values). It carries no domain-predictive signal and would introduce artificial high-cardinality noise if included in model features.

---

## 5. Numerical Features

The system identifies 3 continuous numerical attributes:
1. `tenure` (integer months)
2. `MonthlyCharges` (continuous dollar amount)
3. `TotalCharges` (continuous accumulated dollar amount)

### Preprocessing Steps for Numerical Features:
* **Imputation:** `SimpleImputer(strategy="median")`
* **Scaling:** `StandardScaler()` (subtract mean, scale to unit variance)

### Multicollinearity Note (`TotalCharges` vs `tenure`):
Phase 3 EDA revealed a strong positive correlation between `TotalCharges` and `tenure` (**r = 0.83**). `TotalCharges` is retained in the preprocessing pipeline for Phase 4. Feature selection or exclusion decisions are explicitly deferred to model evaluation (Phases 5–7), as tree-based models and linear models handle multicollinearity differently.

---

## 6. Categorical Features

The system identifies 16 categorical features:
`gender`, `SeniorCitizen`, `Partner`, `Dependents`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`.

### Preprocessing Steps for Categorical Features:
* **Encoder:** `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`
* **Handling Unseen Categories:** Configured with `handle_unknown="ignore"` to ensure zero-filled vectors when novel categorical values appear during real-time inference.

---

## 7. Missing Value Strategy

* **Identified Missing Data:** 11 missing values in `TotalCharges` (corresponding to customers with `tenure == 0`).
* **Imputation Strategy:** `SimpleImputer(strategy="median")` fitted **strictly on `X_train`**.
* **Imputation Statistic:** Calculated exclusively from the training partition to eliminate data leakage.

---

## 8. Train / Test Split

* **Split Ratio:** 80% Training (`X_train`: 5,634 rows) / 20% Testing (`X_test`: 1,409 rows)
* **Random State:** `random_state=42`
* **Stratification:** Stratified by `y` (`stratify=y`)

| Dataset Partition | Total Records | Class 0 (No) Count (%) | Class 1 (Yes) Count (%) |
| :--- | :--- | :--- | :--- |
| **Full Dataset** | 7,043 | 5,174 (73.46%) | 1,869 (26.54%) |
| **Training Set (`X_train`)** | 5,634 | 4,139 (73.46%) | 1,495 (26.54%) |
| **Testing Set (`X_test`)** | 1,409 | 1,035 (73.46%) | 374 (26.54%) |

---

## 9. Preprocessing Pipeline Architecture

The preprocessing logic is implemented as a scikit-learn `ColumnTransformer`:

```
                               Raw Features (19)
                                       │
                      ┌────────────────┴────────────────┐
                      │                                 │
                      ▼                                 ▼
             Numerical Features (3)           Categorical Features (16)
                      │                                 │
            SimpleImputer(median)                       │
                      │                                 │
               StandardScaler()              OneHotEncoder(handle_unknown='ignore')
                      │                                 │
                      └────────────────┬────────────────┘
                                       ▼
                           Transformed Matrix (46 cols)
```

---

## 10. Leakage Prevention

Strict data leakage prevention rules were enforced throughout Phase 4:

1. **Split First, Fit Second:** Train/test split was executed *before* fitting any imputer, scaler, or encoder.
2. **`X_train` Only Fitting:** `preprocessor.fit(X_train)` was called exclusively on training data.
3. **`X_test` Transformation:** `preprocessor.transform(X_test)` applied fitted parameters without refitting.
4. **Target Isolation:** Target `y` was separated prior to feature matrix construction.

---

## 11. Transformed Feature Summary

* **Raw Feature Attributes:** 19
* **Transformed Preprocessed Features:** **46 columns**
  * 3 scaled numerical columns (`num__tenure`, `num__MonthlyCharges`, `num__TotalCharges`)
  * 43 one-hot encoded binary columns (e.g. `cat__Contract_Month-to-month`, `cat__InternetService_Fiber optic`)

---

## 12. Validation Results

All documented preprocessing validation checks passed successfully:

1. **Raw Row Count:** Preserved at 7,043 rows.
2. **Target Encoding:** Strictly binary `{0, 1}`.
3. **Identifier Exclusion:** `customerID` absent from feature matrix `X`.
4. **Numeric Conversion:** `TotalCharges` converted to `float64`.
5. **Missing Values:** 0 NaN values remaining in `X_train_proc` and `X_test_proc`.
6. **Dimension Shapes:** `X_train_proc` is `(5634, 46)`; `X_test_proc` is `(1409, 46)`.
7. **Stratification:** Class ratio exact across training and test splits.
8. **Feature Names:** 46 feature column names retrieved cleanly via `get_feature_names_out()`.
9. **Leakage Verification:** Imputer/scaler parameters derived strictly from `X_train`.
10. **Modular Code Test:** `src/preprocessing.py` verified via automated import test.
11. **Raw Data Protection:** `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` remains untouched.

---

## 13. Decisions Deferred to Model Training

The following decisions were intentionally deferred to Phases 5–8:
* **No ML models trained:** No Logistic Regression, Decision Tree, or Random Forest models fitted.
* **No hyperparameter tuning:** No grid search or cross-validation tuning performed.
* **No feature selection:** `TotalCharges` retained alongside `tenure`.
* **No class rebalancing:** SMOTE, undersampling, or class weighting deferred to Phase 5–7 model training.
* **No pipeline serialization:** Model artifact saving deferred to Phase 10.
