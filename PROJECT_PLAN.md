# Project Plan: Customer Churn Prediction & Business Intelligence System

This document outlines the 17-phase execution roadmap for developing the Customer Churn Prediction & Business Intelligence System.

---

## Phase Overview & Execution Roadmap

### Phase 1 — Project Definition & Governance
* **Objective:** Establish project requirements, system architecture, governance rules, and documentation standards prior to writing code.
* **Main Tasks:**
  * Define functional and non-functional requirements.
  * Formulate high-level system architecture and component boundaries.
  * Draft project README, architecture diagrams, and requirements specifications.
  * Setup version control repository structure.
* **Expected Deliverables:**
  * `README.md`
  * `PROJECT_PLAN.md`
  * `ARCHITECTURE.md`
  * `docs/requirements.md`

### Phase 2 — Dataset & Data Understanding
* **Objective:** Acquire, verify, and inspect historical customer churn dataset for structure, missingness, and data types.
* **Main Tasks:**
  * Obtain public/standard customer churn dataset (e.g., Telco Customer Churn).
  * Load and inspect dataset schema, column definitions, data types, and target distributions.
  * Document missing values, duplicate records, and potential data quality issues.
* **Expected Deliverables:**
  * Raw dataset in designated `data/raw/` directory.
  * Data summary document / initial data dictionary.

### Phase 3 — Exploratory Data Analysis (EDA)
* **Objective:** Discover empirical patterns, correlations, distributions, and churn associations in the historical data.
* **Main Tasks:**
  * Perform univariate analysis on numerical and categorical features.
  * Conduct bivariate analysis comparing features against the churn target variable.
  * Generate visualization plots (histograms, boxplots, bar charts, correlation heatmaps).
  * Summarize key business findings and churn risk indicators.
* **Expected Deliverables:**
  * Comprehensive EDA notebook / analysis report.
  * Exported exploratory visualization charts (`reports/figures/`).

### Phase 4 — Data Preprocessing & Feature Engineering
* **Objective:** Build robust, leak-free feature transformation pipelines suitable for ML classification models.
* **Main Tasks:**
  * Implement train/test split prior to any fitting or transformation.
  * Handle missing data imputations deterministically.
  * Encode categorical attributes (One-Hot / Ordinal Encoding).
  * Scale numerical features where appropriate (StandardScaler / MinMaxScaler).
  * Construct clean `scikit-learn` ColumnTransformer / Pipeline.
* **Expected Deliverables:**
  * Modular preprocessing scripts (`src/preprocessing/`).
  * Reusable scikit-learn Pipeline logic.

### Phase 5 — Baseline ML Model Development
* **Objective:** Establish a benchmark ML model to define performance baselines.
* **Main Tasks:**
  * Implement a simple Logistic Regression baseline classifier.
  * Fit model on training split using the preprocessing pipeline.
  * Evaluate baseline performance on test split across key metrics.
* **Expected Deliverables:**
  * Baseline model training script.
  * Baseline metric evaluation log.

### Phase 6 — Multiple Model Training
* **Objective:** Train multiple candidate machine learning model families on the preprocessed training set.
* **Main Tasks:**
  * Train Decision Tree Classifier.
  * Train Random Forest Classifier.
  * Maintain consistent cross-validation folds across all candidate models.
  * Log training timing and basic cross-validation statistics.
* **Expected Deliverables:**
  * Multi-model training module (`src/models/train.py`).
  * Cross-validation results summary.

### Phase 7 — Model Evaluation & Selection
* **Objective:** Rigorously evaluate model candidates on test data to select the optimal production model based on empirical metrics and business tradeoffs.
* **Main Tasks:**
  * Calculate Accuracy, Precision, Recall, F1-Score, and ROC-AUC for each model.
  * Generate and plot Confusion Matrices and ROC Curves.
  * Analyze false positive vs. false negative business costs.
  * Select the champion model pipeline based on empirical performance.
* **Expected Deliverables:**
  * Comparative model evaluation report and matrix tables.
  * Visual ROC and Confusion Matrix plots.

### Phase 8 — Hyperparameter Tuning
* **Objective:** Optimize selected model hyperparameters using systematic search techniques.
* **Main Tasks:**
  * Perform Grid Search or Random Search with Stratified K-Fold Cross-Validation.
  * Evaluate parameter impact on key metrics (F1-score / Recall / ROC-AUC).
  * Finalize hyperparameter configurations for the champion model.
* **Expected Deliverables:**
  * Hyperparameter tuning script (`src/models/tune.py`).
  * Tuned model configuration artifact.

### Phase 9 — Model Interpretability & Business Insights
* **Objective:** Analyze feature importance metrics to extract business-oriented patterns associated with churn risk.
* **Main Tasks:**
  * Extract feature importance from Tree-based models or coefficients from Logistic Regression.
  * Document top features associated with customer churn.
  * Frame findings around predictive probabilities and statistical relationships (avoiding unsupported causal claims).
* **Expected Deliverables:**
  * Feature importance analysis report and visualizations.

### Phase 10 — ML Pipeline Persistence & Inference Logic
* **Objective:** Package and serialize the complete preprocessing and tuned model pipeline for reproducible API inference.
* **Main Tasks:**
  * Export fitted pipeline as a serialized artifact (e.g., Joblib file).
  * Build standalone inference service module that accepts raw dict/JSON input and outputs prediction + probability + risk tier.
  * Verify inference output against known sample inputs.
* **Expected Deliverables:**
  * Serialized pipeline file (`models/churn_pipeline.joblib`).
  * Predictor interface module (`src/services/inference.py`).

### Phase 11 — FastAPI Backend Development
* **Objective:** Implement a lightweight, performant REST API serving model predictions, analytics data, and metadata.
* **Main Tasks:**
  * Setup FastAPI application with standard router structure.
  * Create Pydantic schemas for request validation and response typing.
  * Implement POST `/api/v1/predict` endpoint for real-time churn prediction.
  * Implement GET `/api/v1/analytics` endpoint for business insights summary.
  * Implement GET `/api/v1/model/info` endpoint for model metadata.
  * Implement health check endpoint GET `/health`.
* **Expected Deliverables:**
  * Functional FastAPI backend codebase (`backend/`).
  * OpenAPI interactive documentation (`/docs`).

### Phase 12 — Database Integration (PostgreSQL / Supabase)
* **Objective:** Enable application-level persistence for logging prediction histories and metadata.
* **Main Tasks:**
  * Setup database client connection using standard Python ORM/driver (e.g., SQLAlchemy or asyncpg).
  * Define table schema for prediction logs (`prediction_id`, `input_features`, `churn_probability`, `churn_prediction`, `risk_level`, `created_at`).
  * Integrate prediction logging into the FastAPI prediction endpoint.
* **Expected Deliverables:**
  * Database migration scripts / schema definitions (`backend/app/db/`).
  * DB service integration with FastAPI endpoints.

### Phase 13 — React Dashboard Frontend Development
* **Objective:** Build an intuitive, modern web dashboard for single-customer churn risk assessment and high-level churn analytics visualization.
* **Main Tasks:**
  * Setup React application stack.
  * Create Single Customer Prediction Form component with real-time API call.
  * Build Prediction Result display with visual risk badge (Low, Medium, High) and probability gauge/bar.
  * Build Business Analytics page visualizing dataset churn breakdowns and feature distributions.
  * Implement clean Navigation, header, and polished visual design system.
* **Expected Deliverables:**
  * React frontend application (`frontend/`).

### Phase 14 — Automated Testing & Quality Assurance
* **Objective:** Verify correctness, stability, and data flow across ML components, API endpoints, and database interactions.
* **Main Tasks:**
  * Write unit tests for data preprocessing and inference modules (`pytest`).
  * Write API route test suites using `httpx` / `TestClient`.
  * Verify Pydantic schema validation for edge cases and bad payload inputs.
* **Expected Deliverables:**
  * Automated test suite under `tests/`.
  * Passing test run reports.

### Phase 15 — Containerization with Docker & Docker Compose
* **Objective:** Package backend API and frontend dashboard into reproducible multi-container environments.
* **Main Tasks:**
  * Write optimized `Dockerfile` for FastAPI backend.
  * Write `Dockerfile` for React frontend.
  * Create `docker-compose.yml` orchestrating backend, frontend, and local PostgreSQL instance.
  * Verify container networking and volume mounts.
* **Expected Deliverables:**
  * `Dockerfile.backend`
  * `Dockerfile.frontend`
  * `docker-compose.yml`

### Phase 16 — Deployment & Infrastructure Readiness
* **Objective:** Configure production build assets, environment variables, and deployment instructions.
* **Main Tasks:**
  * Configure environment variable handling (`.env.example`).
  * Validate production build pipelines for React app and FastAPI server.
  * Document deployment procedures for cloud container hosts (e.g., Render, Railway, GCP Cloud Run, Supabase DB).
* **Expected Deliverables:**
  * Validated deployment configurations and instructions.

### Phase 17 — Documentation & Portfolio Preparation
* **Objective:** Finalize project showcase materials, architectural write-ups, and portfolio presentation.
* **Main Tasks:**
  * Update final metric tables and architectural diagrams in documentation.
  * Prepare clean portfolio summary highlighting engineering decisions, trade-offs, and empirical findings.
  * Conduct full end-to-end repository audit for code quality and cleanliness.
* **Expected Deliverables:**
  * Complete, professional repository ready for portfolio presentation.
