# -*- coding: utf-8 -*-
"""
views/4_modelling.py
Model Training Arena, Scenario Toggle (Early Warning vs Full Term),
Cross-Validation Leaderboard, and Baseline Performance Comparison.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from core.data import load_cohort_dataframe, get_feature_matrices
from core.modeling import train_benchmark_arena
from core.config import COLORS


def render() -> None:
    st.title("Arena Pemodelan & Tolok Ukur (*Model Leaderboard*)")
    st.caption("Pelatihan terstandarisasi 8 algoritma klasifikasi dengan validasi silang bertingkat (Stratified 5-Fold CV)")

    df = load_cohort_dataframe()

    # Settings Panel
    st.markdown("### 1. Konfigurasi Eksperimen & Skenario Waktu")
    c1, c2, c3 = st.columns(3)
    with c1:
        scenario = st.selectbox(
            "Pilih Skenario Prediksi",
            options=["full_term", "early_warning"],
            format_func=lambda s: "Full Term (Seluruh Tugas A1-A7)" if s == "full_term" else "Early Warning (Tugas Awal A1-A3)",
            help="Skenario Early Warning hanya menggunakan interaksi minggu awal sebelum ujian pertama berlangsung."
        )
    with c2:
        imbalance_method = st.selectbox(
            "Penanganan Ketidakseimbangan Kelas",
            options=["class_weight", "smote"],
            format_func=lambda m: "Penyesuaian Bobot (class_weight='balanced')" if m == "class_weight" else "SMOTE Resampling (Dalam Fold)",
            help="Menyesuaikan bobot kelas 36% At-Risk vs 64% Normal."
        )
    with c3:
        n_splits = st.slider("Jumlah Lipatan Validasi Silang (Stratified K-Fold)", min_value=3, max_value=10, value=5)

    X, y, feature_names = get_feature_matrices(df, scenario=scenario)

    st.markdown(
        f"""
        <div class="alert-box alert-info">
            <strong>Status Konfigurasi:</strong> Skenario <code>{scenario.upper()}</code> aktif dengan 
            <strong>{len(feature_names)} fitur input</strong>, <strong>{len(X)} sampel mahasiswa</strong>, 
            dan <strong>Stratified {n_splits}-Fold CV</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Train Button & Execution
    train_clicked = st.button("Latih Seluruh Model Sekarang", type="primary")

    # Store or retrieve leaderboard from session_state
    session_key = f"leaderboard_{scenario}_{imbalance_method}_{n_splits}"
    if train_clicked or session_key not in st.session_state:
        with st.spinner("Menjalankan pipeline cross-validation paralel untuk 8 algoritma..."):
            leaderboard_df = train_benchmark_arena(
                X, y, imbalance_method=imbalance_method, n_splits=n_splits
            )
            st.session_state[session_key] = leaderboard_df
            st.session_state["active_scenario"] = scenario
            st.session_state["active_imbalance"] = imbalance_method

    leaderboard_df = st.session_state[session_key]

    st.divider()

    # Section 2: Sortable Leaderboard Table
    st.markdown("### 2. Klasemen Evaluasi Model (*Sortable Leaderboard*)")
    st.caption("Tabel metrik evaluasi lengkap. Klik header kolom untuk mengurutkan:")

    display_cols = [
        "Algoritma Model",
        "F1-Macro (Mean ± Std)",
        "Balanced Acc",
        "Recall At-Risk",
        "ROC-AUC",
        "MCC",
        "Waktu Fit (s)",
    ]
    st.dataframe(
        leaderboard_df[display_cols],
        width="stretch",
        hide_index=True,
    )

    # Section 3: Visual Comparison vs Baseline
    st.markdown("### 3. Perbandingan Performa Algoritma vs Baseline Acak")

    best_model_name = leaderboard_df.iloc[0]["Algoritma Model"]
    best_f1 = leaderboard_df.iloc[0]["_raw_f1"]
    base_f1 = leaderboard_df[leaderboard_df["Algoritma Model"] == "Majority Baseline"]["_raw_f1"].values[0]
    improvement_pct = ((best_f1 - base_f1) / (base_f1 + 1e-5)) * 100

    st.markdown(
        f"""
        <div class="alert-box alert-success">
            <strong>Model Unggulan:</strong> <code>{best_model_name}</code> meraih skor F1-Macro tertinggi 
            <strong>{best_f1:.3f}</strong>, menunjukkan peningkatan <strong>+{improvement_pct:.1f}%</strong> 
            dibandingkan baseline mayoritas ({base_f1:.3f}).
        </div>
        """,
        unsafe_allow_html=True,
    )

    chart_df = leaderboard_df.copy()
    chart_df["F1-Score"] = chart_df["_raw_f1"]
    fig_bar = px.bar(
        chart_df,
        x="Algoritma Model",
        y="F1-Score",
        color="Algoritma Model",
        color_discrete_map={
            best_model_name: COLORS["primary"],
            "Majority Baseline": "#94a3b8",
        },
        title=f"Perbandingan F1-Macro antar Model (Skenario: {scenario.title()})",
        text_auto=".3f",
    )
    fig_bar.update_layout(
        template="plotly_white",
        showlegend=False,
        plot_bgcolor="#ffffff",
        margin=dict(l=40, r=20, t=50, b=40),
        height=380,
    )
    fig_bar.update_yaxes(range=[0, 1.0], showgrid=True, gridcolor=COLORS["grid"])
    st.plotly_chart(fig_bar, width="stretch", config={"displayModeBar": False})


if __name__ == "__main__":
    render()
