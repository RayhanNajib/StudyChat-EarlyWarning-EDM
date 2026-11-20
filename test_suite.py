# -*- coding: utf-8 -*-
"""
test_suite.py
Verification test suite for Educational Data Mining Early-Warning Testbed.
Tests data integrity, pipeline execution, zero leakage, model training, and view execution.
"""
import sys
import os
import importlib

# Add project root to sys.path
sys.path.insert(0, r"c:\Users\WA\Downloads\TUGAS PKKMB\Data Science")

def test_data_and_features():
    print("[1] Testing data loading & feature engineering...")
    from core.data import load_cohort_dataframe, get_feature_matrices
    from core.config import TARGET_COLUMN

    df = load_cohort_dataframe()
    assert len(df) == 175, f"Expected 175 rows, got {len(df)}"
    assert TARGET_COLUMN in df.columns, f"Target column {TARGET_COLUMN} not in dataframe"
    assert "conceptual_to_code_ratio" in df.columns, "Engineered feature 1 missing"
    assert "error_persistence_index" in df.columns, "Engineered feature 2 missing"
    assert "early_engagement_share" in df.columns, "Engineered feature 3 missing"
    assert "competence_gap" in df.columns, "Competence gap missing"

    # Test full term feature matrix
    X_full, y_full, full_cols = get_feature_matrices(df, scenario="full_term")
    assert len(X_full) == 175
    assert "no_llm_score" not in full_cols, "CRITICAL: no_llm_score leaked into X!"
    assert "llm_score" not in full_cols, "CRITICAL: llm_score leaked into X!"
    assert "cluster_k3" not in full_cols, "CRITICAL: cluster_k3 leaked into X!"

    # Test early warning feature matrix
    X_early, y_early, early_cols = get_feature_matrices(df, scenario="early_warning")
    assert len(X_early) == 175
    assert "early_turns" in early_cols

    print("    PASSED: Data loading, feature matrices, and zero-leakage verified.")


def test_modeling_arena():
    print("[2] Testing multi-model cross validation arena...")
    from core.data import load_cohort_dataframe, get_feature_matrices
    from core.modeling import train_benchmark_arena, get_trained_evaluation_artifacts

    df = load_cohort_dataframe()
    X, y, _ = get_feature_matrices(df, scenario="early_warning")

    # Run quick 3-fold benchmark arena
    leaderboard = train_benchmark_arena(X, y, imbalance_method="class_weight", n_splits=3)
    assert len(leaderboard) >= 7, f"Expected at least 7 models, got {len(leaderboard)}"
    assert "Algoritma Model" in leaderboard.columns
    assert "F1-Macro (Mean ± Std)" in leaderboard.columns
    print(f"    Leaderboard top model: {leaderboard.iloc[0]['Algoritma Model']}")

    # Test evaluation artifacts
    artifacts = get_trained_evaluation_artifacts("Random Forest", X, y, imbalance_method="class_weight", test_size=0.25)
    assert artifacts["cm"].shape == (2, 2), "Confusion matrix shape invalid"
    assert len(artifacts["importance_df"]) == len(X.columns), "Permutation importance feature count mismatch"
    print("    PASSED: Modeling arena and diagnostic artifacts verified.")


def test_view_imports():
    print("[3] Testing view modules import and syntax...")
    view_names = [
        "1_overview",
        "2_exploration",
        "3_preparation",
        "4_modelling",
        "5_evaluation",
        "6_prediction",
        "7_recommendations",
    ]

    for name in view_names:
        mod = importlib.import_module(f"views.{name}")
        assert hasattr(mod, "render"), f"Module views.{name} does not have render() function"
        print(f"    Loaded views/{name}.py successfully.")
    print("    PASSED: All 7 view modules successfully imported.")


if __name__ == "__main__":
    test_data_and_features()
    test_modeling_arena()
    test_view_imports()
    print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
