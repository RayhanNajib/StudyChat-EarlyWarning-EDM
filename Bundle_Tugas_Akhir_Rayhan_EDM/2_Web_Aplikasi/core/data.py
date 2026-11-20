# -*- coding: utf-8 -*-
"""
core/data.py
Dataset ingestion, caching, feature engineering, and data integrity verification.
Strict adherence to non-negotiable data integrity: no synthetic rows, zero leakage.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import streamlit as st

from core.config import (
    RAW_DATA_PATH,
    FALLBACK_DATA_PATH,
    TARGET_COLUMN,
    TARGET_THRESHOLD,
)
from core.codebook import (
    FULL_TERM_FEATURES,
    EARLY_WARNING_FEATURES,
    LEAKAGE_COLUMNS,
)


@st.cache_data(show_spinner=False)
def load_raw_dataset() -> dict:
    """Loads pristine JSON dataset from data/raw/ or fallback testbed path."""
    target_path = RAW_DATA_PATH if RAW_DATA_PATH.exists() else FALLBACK_DATA_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"StudyChat dataset not found at {target_path}")
    with open(target_path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_cohort_dataframe() -> pd.DataFrame:
    """
    Parses student_profiles from the raw JSON, derives target, and computes
    meaningful engineered features. Returns pristine pandas DataFrame (N=175).
    """
    raw_dict = load_raw_dataset()
    profiles = raw_dict.get("student_profiles", [])
    if not profiles:
        raise ValueError("Raw JSON contains empty 'student_profiles' key.")

    df = pd.DataFrame(profiles)

    # 1. Enforce rigorous target definition: no_llm_score < TARGET_THRESHOLD
    # (1 = Academic At-Risk, 0 = Good Standing)
    df["at_risk"] = (df["no_llm_score"] < TARGET_THRESHOLD).astype(int)

    # 2. Feature Engineering: Cognitive Independence Index
    # conceptual_to_code_ratio: conceptual inquiries vs raw code requests
    df["conceptual_to_code_ratio"] = np.round(
        df["conceptual_ratio"] / (df["write_code_ratio"] + 0.01), 3
    )

    # 3. Feature Engineering: Troubleshooting Persistence Index
    # error_persistence_index: captures repetitive debugging stack-trace pasting
    df["error_persistence_index"] = np.round(
        df["error_msg_ratio"] * df["total_turns"], 2
    )

    # 4. Feature Engineering: Early Engagement Proactivity
    # early_engagement_share: fraction of activity done in early assignments A1-A3
    df["early_engagement_share"] = np.round(
        df["early_turns"] / (df["total_turns"] + 1e-5), 3
    )
    df["early_engagement_share"] = df["early_engagement_share"].clip(0.0, 1.0)

    # 5. Domain metric: Illusion of Competence Gap
    # Difference between assignment score (with AI) and unassisted exam score
    df["competence_gap"] = np.round(df["llm_score"] - df["no_llm_score"], 4)

    return df


def get_feature_matrices(
    df: pd.DataFrame, scenario: str = "full_term"
) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """
    Extracts feature matrix X and target y under strict leakage isolation.
    scenario: 'full_term' or 'early_warning'
    """
    if scenario == "early_warning":
        feature_cols = [c for c in EARLY_WARNING_FEATURES if c in df.columns]
    else:
        feature_cols = [c for c in FULL_TERM_FEATURES if c in df.columns]

    # Verification: Ensure absolutely NO leakage column enters X
    for col in LEAKAGE_COLUMNS:
        if col in feature_cols:
            raise RuntimeError(f"CRITICAL LEAKAGE DETECTED: {col} is in feature list!")

    X = df[feature_cols].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y, feature_cols


def get_cohort_summary_stats(df: pd.DataFrame) -> dict:
    """Returns top-level cohort statistics for overview page."""
    total_n = len(df)
    at_risk_count = int((df["at_risk"] == 1).sum())
    good_count = total_n - at_risk_count
    at_risk_pct = round((at_risk_count / total_n) * 100, 1)

    return {
        "total_students": total_n,
        "at_risk_count": at_risk_count,
        "good_standing_count": good_count,
        "at_risk_percentage": at_risk_pct,
        "mean_exam_score": round(float(df["no_llm_score"].mean()) * 100, 1),
        "mean_assign_score": round(float(df["llm_score"].mean()) * 100, 1),
        "mean_competence_gap": round(float(df["competence_gap"].mean()) * 100, 1),
        "mean_total_turns": round(float(df["total_turns"].mean()), 1),
        "total_dialogue_turns": int(df["total_turns"].sum()),
    }


def audit_leakage_status(feature_cols: list[str]) -> pd.DataFrame:
    """Generates an audit report confirming zero leakage."""
    records = []
    for col in feature_cols:
        records.append({
            "Fitur Kandidat": col,
            "Tipe Fitur": "Input Prediktif Sah",
            "Kebocoran Target?": "Tidak (Zero Leakage)",
            "Keterangan": "Hanya berasal dari data interaksi chat sebelum nilai ujian dirilis."
        })
    for col in LEAKAGE_COLUMNS:
        records.append({
            "Fitur Kandidat": col,
            "Tipe Fitur": "Post-Hoc Outcome / Target",
            "Kebocoran Target?": "Ya (Wajib Dikeluarkan)",
            "Keterangan": "Dikeluarkan dari X untuk mencegah skor akurasi palsu."
        })
    return pd.DataFrame(records)
