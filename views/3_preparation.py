# -*- coding: utf-8 -*-
"""
views/3_preparation.py
Data Preprocessing, Feature Engineering, Zero-Leakage Audit, and Transformation Previews.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler

from core.data import load_cohort_dataframe, get_feature_matrices, audit_leakage_status
from core.config import COLORS


def render() -> None:
    st.title("Preparasi Data & Rekayasa Fitur (*Feature Engineering*)")
    st.caption("Standardisasi, isolasi kebocoran target, dan formulasi metrik kemandirian kognitif")

    df = load_cohort_dataframe()

    # Section 1: Feature Engineering Rationale
    st.markdown("### 1. Rekayasa Fitur Kognitif Baru (*Engineered Features*)")
    st.markdown(
        """
        Untuk melampaui analisis frekuensi mentah pada paper terdahulu, kita memformulasikan 
        **3 fitur komposit baru** yang menangkap kualitas interaksi dialog mahasiswa:
        """
    )

    feat_docs = pd.DataFrame([
        {
            "Nama Fitur Rekayasa": "conceptual_to_code_ratio",
            "Label Nomenklatur": "Cognitive Independence Index",
            "Formulasi Matematis": "conceptual_ratio / (write_code_ratio + 0.01)",
            "Rasional Pedagogis": "Mengukur rasio pertanyaan konseptual terhadap permintaan pembuatan kode langsung. Nilai tinggi menandakan mahasiswa yang aktif berpikir, bukan sekadar menggunakan AI sebagai mesin pembuat kode."
        },
        {
            "Nama Fitur Rekayasa": "error_persistence_index",
            "Label Nomenklatur": "Troubleshooting Persistence",
            "Formulasi Matematis": "error_msg_ratio * total_turns",
            "Rasional Pedagogis": "Mengukur intensitas absolut mahasiswa terjebak dalam lingkaran pesan error. Mahasiswa yang berulang kali menempel pesan error tanpa perbaikan konsep memiliki probabilitas gagal tinggi."
        },
        {
            "Nama Fitur Rekayasa": "early_engagement_share",
            "Label Nomenklatur": "Early Engagement Proactivity",
            "Formulasi Matematis": "early_turns / (total_turns + 1e-5)",
            "Rasional Pedagogis": "Mengukur persentase keaktifan yang diselesaikan di awal semester (A1-A3). Mengidentifikasi mahasiswa yang belajar secara teratur vs mahasiswa yang menumpuk pekerjaan di akhir semester."
        }
    ])
    st.dataframe(feat_docs, width="stretch", hide_index=True)

    st.divider()

    # Section 2: Zero-Leakage Audit Verification
    st.markdown("### 2. Audit Verifikasi Bebas Kebocoran Target (*Zero-Leakage Audit*)")
    st.markdown(
        """
        <div class="alert-box alert-success">
            <strong>Integritas Metodologis Terverifikasi:</strong> Seluruh variabel nilai ujian mandiri 
            (<code>no_llm_score</code>), nilai tugas (<code>llm_score</code>), nilai akhir (<code>overall_score</code>), 
            dan klaster post-hoc (<code>cluster_k3</code>) <strong>secara ketat dikeluarkan</strong> dari matriks fitur input (X).
        </div>
        """,
        unsafe_allow_html=True,
    )

    X_full, y_full, feature_names = get_feature_matrices(df, scenario="full_term")
    leak_audit_df = audit_leakage_status(feature_names)
    st.dataframe(leak_audit_df, width="stretch", hide_index=True)

    st.divider()

    # Section 3: Before vs After Transformation Preview
    st.markdown("### 3. Pratinjau Transformasi (*Before vs After Scaling*)")
    st.caption("Perbandingan nilai numerik mentah vs hasil standardisasi Z-score (StandardScaler):")

    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("##### Sebelum Scaling (Fitur Asli):")
        st.dataframe(X_full.head(6), width="stretch")
    with c_right:
        st.markdown("##### Setelah Scaling (StandardScaler mean=0, std=1):")
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X_full), columns=X_full.columns, index=X_full.index)
        st.dataframe(X_scaled.round(3).head(6), width="stretch")

    st.divider()

    # Section 4: Correlation Matrix
    st.markdown("### 4. Matriks Korelasi Antar-Fitur Input (Pearson)")
    st.caption("Pemeriksaan multikolinearitas antar fitur masukan prediktif:")
    corr = X_full.corr().round(2)
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1.0,
        zmax=1.0,
        title="Matriks Korelasi Pearson Fitur Masukan (Zero-Leakage)",
    )
    fig_corr.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor="#ffffff",
        height=480,
    )
    st.plotly_chart(fig_corr, width="stretch", config={"displayModeBar": False})


if __name__ == "__main__":
    render()
