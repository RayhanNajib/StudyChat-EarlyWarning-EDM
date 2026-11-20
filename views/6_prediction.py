# -*- coding: utf-8 -*-
"""
views/6_prediction.py
Interactive Early-Warning Risk Simulator:
Real-time inference form, preset student profiles, probability gauge, and driving factors.
"""
import streamlit as st
import pandas as pd
import numpy as np

from core.data import load_cohort_dataframe, get_feature_matrices
from core.modeling import get_trained_evaluation_artifacts
from core.config import COLORS
from core.ui import render_metric_card


def render() -> None:
    st.title("Simulasi & Inferensi Dini Mahasiswa (*Real-Time Risk Inference*)")
    st.caption("Uji profil interaksi mahasiswa baru untuk memprediksi risiko kegagalan pada ujian mandiri")

    df = load_cohort_dataframe()
    X, y, feature_names = get_feature_matrices(df, scenario="full_term")

    # Fit a high-reliability model for simulation
    artifacts = get_trained_evaluation_artifacts(
        "Random Forest", X, y, imbalance_method="class_weight", test_size=0.25
    )
    pipeline = artifacts["pipeline"]

    st.markdown("### 1. Pilih Profil Contoh atau Masukkan Data Manual")

    preset = st.radio(
        "Pilih Profil Preset Simulasi:",
        options=[
            "Manual (Kustom)",
            "Profil A: Mahasiswa Mandiri (High Conceptual Inquirer)",
            "Profil B: Mahasiswa Terjebak Error (High Error & Code Copier)",
            "Profil C: Mahasiswa Pasif (Low Turns, Minimalist)",
        ],
        horizontal=True,
    )

    # Set default values based on preset
    if preset == "Profil A: Mahasiswa Mandiri (High Conceptual Inquirer)":
        d_turns, d_assign = 110, 6
        d_p_len, d_r_len = 1200.0, 2800.0
        d_conc, d_code, d_err, d_ctx = 0.45, 0.08, 0.02, 0.15
        d_early_turns = 60
    elif preset == "Profil B: Mahasiswa Terjebak Error (High Error & Code Copier)":
        d_turns, d_assign = 130, 4
        d_p_len, d_r_len = 750.0, 2200.0
        d_conc, d_code, d_err, d_ctx = 0.08, 0.35, 0.28, 0.20
        d_early_turns = 30
    elif preset == "Profil C: Mahasiswa Pasif (Low Turns, Minimalist)":
        d_turns, d_assign = 18, 2
        d_p_len, d_r_len = 450.0, 1500.0
        d_conc, d_code, d_err, d_ctx = 0.10, 0.20, 0.05, 0.10
        d_early_turns = 8
    else:
        d_turns, d_assign = 80, 5
        d_p_len, d_r_len = 950.0, 2500.0
        d_conc, d_code, d_err, d_ctx = 0.22, 0.12, 0.06, 0.24
        d_early_turns = 45

    st.markdown("#### Parameter Interaksi Chatbot Mahasiswa")
    col1, col2, col3 = st.columns(3)
    with col1:
        in_turns = st.number_input("Total Tuturan Chat (total_turns)", min_value=1, max_value=500, value=int(d_turns))
        in_early_turns = st.number_input("Tuturan Tugas Awal (early_turns)", min_value=0, max_value=in_turns, value=int(min(d_early_turns, in_turns)))
        in_assign = st.number_input("Jumlah Tugas Aktif (assignments_count)", min_value=1, max_value=7, value=int(d_assign))
    with col2:
        in_conc = st.slider("Rasio Pertanyaan Konsep (conceptual_ratio)", 0.0, 1.0, float(d_conc), step=0.01)
        in_code = st.slider("Rasio Permintaan Kode (write_code_ratio)", 0.0, 1.0, float(d_code), step=0.01)
        in_err = st.slider("Rasio Paste Pesan Error (error_msg_ratio)", 0.0, 1.0, float(d_err), step=0.01)
    with col3:
        in_ctx = st.slider("Rasio Pertanyaan Kontekstual (contextual_ratio)", 0.0, 1.0, float(d_ctx), step=0.01)
        in_p_len = st.number_input("Rata-rata Panjang Prompt (chars)", min_value=10.0, max_value=5000.0, value=float(d_p_len))
        in_r_len = st.number_input("Rata-rata Panjang Respon AI (chars)", min_value=10.0, max_value=8000.0, value=float(d_r_len))

    # Compute engineered features
    eng_indep = round(in_conc / (in_code + 0.01), 3)
    eng_err_persist = round(in_err * in_turns, 2)
    eng_early_share = round(in_early_turns / (in_turns + 1e-5), 3)

    record_dict = {
        "total_turns": in_turns,
        "assignments_count": in_assign,
        "avg_prompt_len": in_p_len,
        "avg_resp_len": in_r_len,
        "conceptual_ratio": in_conc,
        "write_code_ratio": in_code,
        "error_msg_ratio": in_err,
        "contextual_ratio": in_ctx,
        "conceptual_to_code_ratio": eng_indep,
        "error_persistence_index": eng_err_persist,
        "early_engagement_share": eng_early_share,
    }

    input_df = pd.DataFrame([record_dict])

    st.divider()

    # Inference Button & Output
    st.markdown("### 2. Hasil Inferensi & Diagnosis Risiko")

    pred_class = pipeline.predict(input_df)[0]
    prob_risk = pipeline.predict_proba(input_df)[0][1] if hasattr(pipeline, "predict_proba") else (1.0 if pred_class == 1 else 0.0)

    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        if pred_class == 1:
            st.markdown(
                f"""
                <div class="alert-box alert-warning">
                    <h3 style="margin: 0; color: #881337;">Prediksi: ACADEMIC AT-RISK</h3>
                    <p style="margin-top: 6px;">Mahasiswa terdeteksi berisiko tinggi gagal pada ujian mandiri tanpa bantuan AI (skor &lt; 85%).</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="alert-box alert-success">
                    <h3 style="margin: 0; color: #064e3b;">Prediksi: GOOD STANDING</h3>
                    <p style="margin-top: 6px;">Pola dialog mengindikasikan kemandirian kognitif yang memadai untuk menghadapi ujian tanpa AI.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with res_col2:
        render_metric_card(
            "Estimasi Probabilitas Risiko Kegagalan",
            f"{prob_risk * 100:.1f}%",
            "Threshold klasifikasi: 50.0%",
            status="at_risk" if prob_risk >= 0.5 else "safe",
        )

    st.divider()

    # Section 3: Diagnostic Breakdown & Top Risk Drivers
    st.markdown("### 3. Faktor Pemicu Utama (*Driving Risk Factors*)")

    diag_rows = [
        {
            "Indikator Kognitif": "Cognitive Independence Index",
            "Nilai Mahasiswa": f"{eng_indep:.2f}",
            "Ambang Batas Ideal": ">= 1.50",
            "Evaluasi Pedagogis": "Tinggi (Mandiri)" if eng_indep >= 1.5 else "Rendah (Tergantung Sintesis Kode)"
        },
        {
            "Indikator Kognitif": "Troubleshooting Persistence",
            "Nilai Mahasiswa": f"{eng_err_persist:.2f}",
            "Ambang Batas Ideal": "< 5.00",
            "Evaluasi Pedagogis": "Aman" if eng_err_persist < 5.0 else "Tinggi (Terjebak Perulangan Error)"
        },
        {
            "Indikator Kognitif": "Early Engagement Proactivity",
            "Nilai Mahasiswa": f"{eng_early_share * 100:.1f}%",
            "Ambang Batas Ideal": ">= 40.0%",
            "Evaluasi Pedagogis": "Proaktif sejak awal" if eng_early_share >= 0.4 else "Pasif / Menunda Tugas"
        }
    ]
    st.dataframe(pd.DataFrame(diag_rows), width="stretch", hide_index=True)


if __name__ == "__main__":
    render()
