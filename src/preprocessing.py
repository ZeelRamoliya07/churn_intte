"""
ML Preprocessing & Feature Engineering Module
Customer Churn Prediction & Business Intelligence System

This module provides reusable, leak-free data loading, target processing,
and feature transformation pipelines using scikit-learn.
"""

import os
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Define expected raw dataset schema
REQUIRED_COLUMNS: List[str] = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"
]


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load the raw Telco customer dataset and validate schema integrity.
    
    Parameters:
        filepath: Path to the raw CSV dataset file.
        
    Returns:
        pd.DataFrame: Loaded dataset.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw dataset file not found at: {filepath}")

    df = pd.read_csv(filepath)

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Raw dataset is missing required columns: {missing_cols}")

    return df


def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and convert TotalCharges column from raw string format to float.
    Whitespace strings are explicitly converted to NaN (np.nan).
    
    Parameters:
        df: Input DataFrame containing TotalCharges.
        
    Returns:
        pd.DataFrame: DataFrame with TotalCharges converted to float.
    """
    df_cleaned = df.copy()
    if "TotalCharges" in df_cleaned.columns:
        df_cleaned["TotalCharges"] = pd.to_numeric(
            df_cleaned["TotalCharges"].astype(str).str.strip(),
            errors="coerce"
        )
    return df_cleaned


def process_target(df: pd.DataFrame, target_col: str = "Churn") -> Tuple[pd.DataFrame, pd.Series]:
    """
    Separate target column and encode 'No' -> 0, 'Yes' -> 1.
    
    Parameters:
        df: Input DataFrame.
        target_col: Name of the target column.
        
    Returns:
        Tuple[pd.DataFrame, pd.Series]: (Features DataFrame X, Target Series y)
        
    Raises:
        ValueError: If target_col contains unexpected values.
    """
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found in dataset.")

    target_values = df[target_col].unique()
    valid_values = {"No", "Yes"}
    if not set(target_values).issubset(valid_values):
        raise ValueError(f"Unexpected values in target column '{target_col}': {target_values}")

    y = df[target_col].map({"No": 0, "Yes": 1}).astype(int)
    X = df.drop(columns=[target_col])

    return X, y


def get_feature_groups(X: pd.DataFrame, identifier_col: str = "customerID") -> Tuple[List[str], List[str]]:
    """
    Identify numerical and categorical feature names after excluding the identifier column.
    
    Parameters:
        X: Feature DataFrame.
        identifier_col: Identifier column name to exclude.
        
    Returns:
        Tuple[List[str], List[str]]: (numerical_features, categorical_features)
    """
    X_features = X.drop(columns=[identifier_col], errors="ignore")
    
    num_features = ["tenure", "MonthlyCharges", "TotalCharges"]
    cat_features = [col for col in X_features.columns if col not in num_features]

    return num_features, cat_features


def build_preprocessing_pipeline(
    num_features: List[str],
    cat_features: List[str]
) -> ColumnTransformer:
    """
    Construct scikit-learn ColumnTransformer for numerical and categorical features.
    
    Numerical Pipeline: SimpleImputer(median) -> StandardScaler()
    Categorical Pipeline: OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    
    Parameters:
        num_features: List of numerical column names.
        cat_features: List of categorical column names.
        
    Returns:
        ColumnTransformer: Unfitted preprocessing ColumnTransformer.
    """
    num_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline(steps=[
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, num_features),
            ("cat", cat_pipeline, cat_features)
        ],
        remainder="drop"
    )

    return preprocessor


def prepare_data_and_pipeline(
    filepath: str,
    test_size: float = 0.2,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Executes complete leak-free data loading, target processing, train/test splitting,
    and preprocessing transformer fitting.
    
    Leakage Prevention Flow:
    Raw Data -> Load & Clean -> Target/Identifier Separation -> Train/Test Split ->
    Fit Preprocessor on X_train ONLY -> Transform X_train & X_test
    
    Parameters:
        filepath: Path to raw dataset CSV.
        test_size: Ratio of test dataset split (default 0.2).
        random_state: Random seed for reproducibility (default 42).
        
    Returns:
        Dict containing split datasets, fitted preprocessor, and metadata.
    """
    # 1. Load raw data
    df_raw = load_raw_data(filepath)

    # 2. Clean TotalCharges
    df_clean = clean_total_charges(df_raw)

    # 3. Target processing
    X_raw, y = process_target(df_clean, target_col="Churn")

    # 4. Exclude identifier column customerID
    X = X_raw.drop(columns=["customerID"], errors="ignore")

    # 5. Train/Test Split (BEFORE fitting any preprocessor)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # 6. Identify feature groups
    num_features, cat_features = get_feature_groups(X_raw)

    # 7. Build unfitted ColumnTransformer
    preprocessor = build_preprocessing_pipeline(num_features, cat_features)

    # 8. Fit ColumnTransformer STRICTLY on X_train
    preprocessor.fit(X_train)

    # 9. Transform X_train and X_test
    X_train_proc = preprocessor.transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # 10. Extract feature names
    feature_names = preprocessor.get_feature_names_out().tolist()

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_train_processed": X_train_proc,
        "X_test_processed": X_test_proc,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
        "num_features": num_features,
        "cat_features": cat_features
    }
