# Requirements Specification: Customer Churn Prediction & Business Intelligence System

---

## 1. Project Objective

The objective of the **Customer Churn Prediction & Business Intelligence System** is to develop an end-to-end machine learning solution that predicts customer churn risk, classifies customers into actionable risk categories, and presents data-driven business intelligence analytics through a web application interface and REST API.

---

## 2. Target Users

1. **Business Analysts & Retention Managers:** Users who require insights into overall customer churn trends, key risk drivers, and risk breakdowns across customer segments to design targeted retention campaigns.
2. **Customer Relationship Representatives:** Users who input individual customer parameters to receive real-time churn probability scores and risk assessments.
3. **API Consumer Systems / Developers:** External applications or internal microservices consuming automated churn risk predictions via REST endpoints.

---

## 3. Problem Statement

Customer churn leads to lost revenue and increased acquisition costs. Organizations often possess rich historical customer interaction data but lack:
* Automated, empirical tools to predict churn probability for specific customers.
* Interpretable risk categorization to prioritize retention interventions.
* Centralized dashboards providing operational visibility into historical churn drivers and prediction logs.

---

## 4. Functional Requirements

* **FR-01 (Dataset Exploration):** The system shall support exploration of historical customer churn datasets, including missing value inspection, attribute distributions, and summary statistics.
* **FR-02 (Data Preprocessing):** The system shall support repeatable data preprocessing suitable for machine learning, including missing value imputation, categorical encoding, and feature scaling.
* **FR-03 (Multiple Model Training):** The system shall support training multiple classification model algorithms (Logistic Regression, Decision Tree, Random Forest) on customer churn data.
* **FR-04 (Multi-Metric Evaluation):** The system shall evaluate trained models using multiple classification metrics (Accuracy, Precision, Recall, F1-score, ROC-AUC, Confusion Matrix).
* **FR-05 (Pipeline Persistence):** The system shall persist the selected trained ML pipeline artifact (preprocessing + model) for reproducible inference.
* **FR-06 (Prediction API):** The backend shall expose a REST API endpoint for real-time customer churn prediction.
* **FR-07 (Churn Probability Output):** The prediction API shall return a numerical churn probability score between 0.00 and 1.00.
* **FR-08 (Predicted Class Output):** The prediction API shall return a predicted binary churn class (0 = Retained, 1 = Churned).
* **FR-09 (Human-Readable Risk Tiering):** The system shall convert raw prediction probability into a human-readable risk category (Low Risk, Medium Risk, High Risk).
* **FR-10 (Churn Analytics Summary):** The system shall provide business analytics summarizing customer churn patterns and feature associations from dataset analysis.
* **FR-11 (Web Dashboard UI):** The web application shall provide an interactive dashboard for business-oriented visual analytics and single-customer risk assessment.
* **FR-12 (Prediction History Persistence):** The system shall maintain application-level prediction history logs in a database for auditability and analytical tracking.
* **FR-13 (Model Metadata Exposure):** The system shall expose endpoints providing model metadata, feature lists, and evaluation performance summaries.

---

## 5. Non-Functional Requirements

* **NFR-01 (Modular Architecture):** The system shall adopt a clean, modular architecture separating ML pipeline logic, backend API services, database operations, and frontend components.
* **NFR-02 (Training-Serving Consistency):** ML preprocessing and real-time inference shall use identical pipeline transformation logic to eliminate training-serving skew.
* **NFR-03 (Input Data Validation):** API input payloads shall be validated using Pydantic schemas before executing model inference.
* **NFR-04 (Informative Error Handling):** The backend API shall provide clear, structured JSON error responses with appropriate HTTP status codes.
* **NFR-05 (Multi-Level Testability):** The system shall support automated testing across ML transformation functions, API endpoints, and database interactions.
* **NFR-06 (Containerizability):** The application stack (backend, frontend, database) shall be containerizable and deployable using Docker and Docker Compose.
* **NFR-07 (Comprehensive Documentation):** The repository shall include thorough setup, architecture, and API documentation to allow straightforward setup and evaluation.
* **NFR-08 (Data Leakage Prevention):** The ML pipeline logic shall strictly enforce train/test split isolation before applying feature transformations or scaling.
* **NFR-09 (Reproducible Artifact Management):** Model artifacts and pipeline configurations shall be versionable and reproducible across training runs.

---

## 6. Machine Learning Requirements

* **Problem Formulation:** Supervised Binary Classification.
* **Target Label:** `Churn` (1 = Churned, 0 = Retained).
* **Candidate Algorithms:**
  1. Logistic Regression (Baseline)
  2. Decision Tree Classifier
  3. Random Forest Classifier
  4. XGBoost Classifier (Optional / Post-MVP)
* **Model Selection Principle:** Model selection will be strictly empirical based on test set metric comparisons (Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix). **Accuracy alone will not govern model selection.** Business tradeoffs regarding false positives vs. false negatives must be documented.
* **Analytical Boundary Principle:** Feature importance and predictive probabilities indicate statistical association within historical data; they do **not** constitute proof of causality.

---

## 7. API Requirements

* **Base URL:** `/api/v1`
* **Endpoints:**
  * `POST /api/v1/predict` — Accepts customer features JSON payload; returns probability, binary prediction class, risk level, and timestamp.
  * `GET /api/v1/analytics` — Returns dataset-level churn metrics and feature distribution summaries.
  * `GET /api/v1/model/info` — Returns metadata regarding active model pipeline (algorithm, version, evaluation metrics, feature names).
  * `GET /health` — Returns system health status.
* **Format:** JSON request body and JSON response payload.
* **Validation:** Mandatory Pydantic schema validation; invalid fields must return `422 Unprocessable Entity`.

---

## 8. Frontend Requirements

* **Framework:** React SPA (Single Page Application).
* **Pages/Views:**
  1. **Churn Predictor View:** Form interface allowing manual entry of customer attributes, triggering real-time API call, and displaying styled risk level badges and probability metrics.
  2. **Analytics Dashboard View:** Visual charts illustrating churn rate breakdowns by demographics, contract types, and service usage.
  3. **Model Information View:** Display showing champion model metrics, confusion matrix visualization, and active version details.
* **UI Design Principles:** Modern aesthetic, visual contrast, responsive layout, clear status indicators.

---

## 9. Database Requirements

* **Database Engine:** PostgreSQL / Supabase.
* **Primary Responsibilities:** Logging application-level prediction outputs and input feature payloads.
* **Table Schema (`prediction_logs`):**
  * `id` (UUID, Primary Key)
  * `customer_id` (VARCHAR(100), Optional)
  * `input_payload` (JSONB / TEXT)
  * `churn_probability` (FLOAT)
  * `predicted_class` (INT)
  * `risk_level` (VARCHAR(20))
  * `created_at` (TIMESTAMP WITH TIME ZONE)

---

## 10. Security Considerations

* CORS middleware configuration on backend API to restrict unauthorized frontend origins.
* Input validation via Pydantic to prevent injection payloads.
* Environment variable isolation for database passwords, API keys, and connection strings (`.env`).
* No plain-text storage of sensitive credentials in version control (`.gitignore` enforcement).

---

## 11. Testing Requirements

* **ML Testing:** Unit tests for data preprocessing functions, feature encoders, and pipeline serialization (`pytest`).
* **Backend Testing:** Integration tests for FastAPI endpoints using `TestClient` / `httpx`, verifying valid inputs, invalid payloads, and error responses.
* **End-to-End Validation:** Verification that sample input payloads return predictable outputs through API routes.

---

## 12. Deployment Requirements

* Dockerfiles for backend and frontend components.
* `docker-compose.yml` for unified local setup (Backend + Frontend + PostgreSQL).
* Environment variable configuration template (`.env.example`).
* Clear deployment instructions for standard cloud platforms (e.g., GCP, Render, Supabase).

---

## 13. MVP Scope Boundaries

### Included in MVP:
1. Dataset cleaning & exploratory analysis documentation.
2. Feature preprocessing pipeline.
3. Training & evaluation of Logistic Regression, Decision Tree, and Random Forest models.
4. Selection and joblib persistence of champion model pipeline.
5. FastAPI REST API endpoints (`/predict`, `/analytics`, `/model/info`, `/health`).
6. Single-customer risk prediction React UI page.
7. Basic business analytics visualization React dashboard.
8. PostgreSQL / Supabase table setup and prediction audit logging.
9. Automated tests for preprocessing and API endpoints.
10. Containerized multi-service configuration via Docker Compose.

---

## 14. Post-MVP & Future Enhancements

* **XGBoost Classifier Evaluation:** Comparative benchmarking of gradient boosting models.
* **SHAP Explainability Integration:** Local and global model explainability using SHAP values.
* **Batch Processing:** Support for uploading CSV files for bulk prediction generation.
* **Model & Data Drift Monitoring:** Tracking performance decay and input distribution shifts over time.
* **Retraining Pipeline Automation:** Scheduled or event-driven model retraining workflows.
* **Authentication & Role-Based Access Control:** Secure user logins and role permissions.
* **Customer Retention Action Recommendation:** Rule-based or AI-assisted retention strategy suggestions based on risk tier.
