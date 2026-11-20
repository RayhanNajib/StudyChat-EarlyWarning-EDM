# -*- coding: utf-8 -*-
"""
views/5_evaluation.py
Detailed Diagnostic Evaluation: Confusion Matrix, ROC/PR Curves,
Per-Class Classification Report, and Permutation Feature Importance.
"""
import streamlit as st
import pandas as pd

from core.data import load_cohort_dataframe, get_feature_matrices
from core.modeling import get_trained_evaluation_artifacts, get_model_catalog
from core.ui import (
    plot_confusion_matrix,
    plot_roc_pr_curves,
    plot_permutation_importance,
    render_metric_card,
)


def render() -> None:
    st.title("Evaluasi Diagnostik & Eksplanabilitas (*Model Diagnostics*)")
    st.caption("Pemeriksaan mendalam matriks konfusi, kurva sensitivitas, dan analisis kepentingan fitur")

    df = load_cohort_dataframe()
    scenario = st.session_state.get("active_scenario", "full_term")
    imbalance = st.session_state.get("active_imbalance", "class_weight")

    X, y, feature_names = get_feature_matrices(df, scenario=scenario)
    available_models = list(get_model_catalog().keys())

    # Model Selector
    c1, c2 = st.columns([2, 1])
    with c1:
        selected_model = st.selectbox(
            "Pilih Model untuk Diagnostik Mendalam",
            options=available_models,
            index=3 if "Random Forest" in available_models else 1,
            help="Menampilkan diagnostik rinci pada data uji terpisah (Holdout Test Set 25%)."
        )
    with c2:
        test_size = st.slider("Ukuran Data Uji Holdout", min_value=0.15, max_value=0.35, value=0.25, step=0.05)

    artifacts = get_trained_evaluation_artifacts(
        selected_model, X, y, imbalance_method=imbalance, test_size=test_size
    )

    # Granular summary metrics for selected model
    rep = artifacts["report"]
    risk_f1 = rep.get("At-Risk", {}).get("f1-score", 0.0)
    risk_rec = rep.get("At-Risk", {}).get("recall", 0.0)
    macro_f1 = rep.get("macro avg", {}).get("f1-score", 0.0)
    auc_val = artifacts["roc_auc"]

    st.markdown("### 1. Ringkasan Kinerja Uji (*Holdout Test Performance*)")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("F1-Macro Uji", f"{macro_f1:.3f}", "Rata-rata tertimbang kelas", status="primary")
    with m2:
        render_metric_card("Recall At-Risk", f"{risk_rec*100:.1f}%", "Mahasiswa rentan terdeteksi", status="at_risk")
    with m3:
        render_metric_card("F1-Score At-Risk", f"{risk_f1:.3f}", "Akurasi presisi-sensitivitas", status="at_risk")
    with m4:
        render_metric_card("ROC-AUC Score", f"{auc_val:.3f}", "Daya diskriminasi global", status="safe")

    st.divider()

    # Section 2: Visual Diagnostics (Confusion Matrix & ROC Curve)
    st.markdown("### 2. Matriks Konfusi & Kurva ROC")
    col_cm, col_roc = st.columns(2)

    with col_cm:
        fig_cm = plot_confusion_matrix(artifacts["cm"], artifacts["cm_norm"])
        st.plotly_chart(fig_cm, width="stretch", config={"displayModeBar": False})
        st.caption("Diagonal utama mencerminkan prediksi benar. Sel kanan atas mencerminkan False Alarm, sel kiri bawah mencerminkan mahasiswa rentan yang luput.")

    with col_roc:
        fig_roc = plot_roc_pr_curves(
            artifacts["fpr"], artifacts["tpr"], artifacts["roc_auc"],
            artifacts["recall_curve"], artifacts["precision_curve"]
        )
        st.plotly_chart(fig_roc, width="stretch", config={"displayModeBar": False})
        st.caption("Kurva ROC menunjukkan trade-off antara True Positive Rate dan False Positive Rate pada berbagai ambang batas klasifikasi.")

    st.divider()

    # Section 3: Per-Class Classification Report Table
    st.markdown("### 3. Laporan Klasifikasi Rinci per Kelas (*Per-Class Report*)")
    report_rows = []
    for k in ["Good Standing", "At-Risk", "macro avg", "weighted avg"]:
        if k in rep:
            report_rows.append({
                "Kategori / Kelas": k,
                "Precision": round(rep[k]["precision"], 3),
                "Recall (Sensitivitas)": round(rep[k]["recall"], 3),
                "F1-Score": round(rep[k]["f1-score"], 3),
                "Jumlah Sampel (Support)": int(rep[k]["support"]),
            })
    st.dataframe(pd.DataFrame(report_rows), width="stretch", hide_index=True)

    st.divider()

    # Section 4: Permutation Feature Importance & Interpretation
    st.markdown("### 4. Kepentingan Fitur (*Permutation Feature Importance*)")
    st.markdown(
        """
        Permutation Importance mengukur seberapa drastis skor model menurun saat suatu fitur diacak secara acak.
        Metode ini tahan terhadap korelasi palsu dan memberikan interpretasi yang adil terhadap kontribusi fitur.
        """
    )

    fig_imp = plot_permutation_importance(artifacts["importance_df"])
    st.plotly_chart(fig_imp, width="stretch", config={"displayModeBar": False})

    st.caption("Fitur dengan penurunan F1 terbesar berada di posisi teratas. Ini membuktikan bahwa fitur kognitif (pertanyaan konseptual dan rasio error) memegang peranan krusial dalam menentukan hasil ujian mandiri.")


if __name__ == "__main__":
    render()
