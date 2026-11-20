# -*- coding: utf-8 -*-
"""
views/2_exploration.py
Exploratory Data Analysis: Illusion of Competence, Cognitive Dialogue Dynamics,
4 Behavioral Personas, and Statistical Significance Testing.
"""
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

from core.data import load_cohort_dataframe
from core.ui import plot_illusion_gap_scatter, plot_dialogue_landscape, render_metric_card


def render() -> None:
    st.title("Eksplorasi Data & Dinamika Dialog Kognitif")
    st.caption("Investigasi pola perilaku tuturan mahasiswa dan fenomena Illusion of Competence")

    df = load_cohort_dataframe()

    # Section 1: Illusion of Competence
    st.markdown("### 1. Fenomena Kesenjangan Nilai (*Illusion of Competence Gap*)")
    st.markdown(
        """
        Banyak mahasiswa meraih nilai tugas pemrograman yang tinggi (rata-rata 94.8%) karena bantuan ChatGPT,
        namun mengalami penurunan drastis saat diuji dalam ujian mandiri tanpa AI (rata-rata 86.3%, dengan batas bawah 33.8%).
        Kesenjangan ini menjadi justifikasi pentingnya deteksi dini risiko akademik.
        """
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("Rata-rata Nilai Tugas (Dengan AI)", f"{df['llm_score'].mean()*100:.1f}%", "Bantuan asisten LLM diizinkan", status="normal")
    with c2:
        render_metric_card("Rata-rata Nilai Ujian (Tanpa AI)", f"{df['no_llm_score'].mean()*100:.1f}%", "Ujian mandiri murni", status="normal")
    with c3:
        render_metric_card("Rata-rata Kesenjangan (Gap)", f"{df['competence_gap'].mean()*100:.1f}%", "Disparitas performa", status="at_risk")

    fig_gap = plot_illusion_gap_scatter(df)
    st.plotly_chart(fig_gap, width="stretch", config={"displayModeBar": False})
    st.caption("Garis putus-putus abu-abu menunjukkan paritas sempurna (nilai tugas = nilai ujian). Titik merah di bawah garis mengindikasikan mahasiswa yang mengalami penurunan performa drastis saat ujian tanpa AI.")

    st.divider()

    # Section 2: Cognitive Dialogue Landscape
    st.markdown("### 2. Lansekap Kognitif: Konseptual vs Jebakan Pesan Error")
    st.markdown(
        """
        Sesuai temuan McNichols et al. (2026), mahasiswa yang mengajukan pertanyaan konseptual cenderung mandiri dan memahami materi,
        sedangkan mahasiswa yang terjebak dalam siklus menyalin pesan error (*error message loops*) mengalami disorientasi belajar.
        """
    )
    fig_land = plot_dialogue_landscape(df)
    st.plotly_chart(fig_land, width="stretch", config={"displayModeBar": False})
    st.caption("Ukuran lingkaran merepresentasikan total volume tuturan dialog (total_turns). Warna merah menunjukkan mahasiswa berisiko (at_risk=1).")

    st.divider()

    # Section 3: Statistical Significance Testing (Two-Sample t-test / Welch's t-test)
    st.markdown("### 3. Uji Signifikansi Statistik Antar Kelompok (At-Risk vs Good Standing)")
    st.markdown(
        """
        Uji Welch's t-test (tidak mengasumsikan varians sama) untuk membuktikan apakah perbedaan fitur perilaku
        antara kelompok mahasiswa berisiko (*At-Risk*) dan mahasiswa aman (*Good Standing*) berbeda secara signifikan secara statistik.
        """
    )

    features_to_test = [
        ("total_turns", "Total Dialogue Turns"),
        ("conceptual_ratio", "Conceptual Question Ratio"),
        ("write_code_ratio", "Write Code Request Ratio"),
        ("error_msg_ratio", "Error Message Pasting Ratio"),
        ("contextual_ratio", "Contextual Question Ratio"),
        ("conceptual_to_code_ratio", "Cognitive Independence Index (Engineered)"),
        ("error_persistence_index", "Troubleshooting Persistence (Engineered)"),
        ("early_engagement_share", "Early Engagement Proactivity (Engineered)"),
    ]

    t_test_records = []
    risk_sub = df[df["at_risk"] == 1]
    safe_sub = df[df["at_risk"] == 0]

    for col, label in features_to_test:
        v_risk = risk_sub[col].dropna()
        v_safe = safe_sub[col].dropna()
        t_stat, p_val = stats.ttest_ind(v_risk, v_safe, equal_var=False)

        mean_risk = v_risk.mean()
        mean_safe = v_safe.mean()
        is_sig = p_val < 0.05

        t_test_records.append({
            "Fitur Perilaku": label,
            "Rata-rata At-Risk": f"{mean_risk:.3f}",
            "Rata-rata Good Standing": f"{mean_safe:.3f}",
            "Nilai t-Statistik": f"{t_stat:.3f}",
            "p-Value": f"{p_val:.4f}",
            "Status Signifikansi (alpha=0.05)": "Signifikan (p < 0.05)" if is_sig else "Tidak Signifikan",
            "Arah Korelasi": "Lebih tinggi pada At-Risk" if mean_risk > mean_safe else "Lebih tinggi pada Good Standing"
        })

    t_test_df = pd.DataFrame(t_test_records)
    st.dataframe(t_test_df, width="stretch", hide_index=True)

    st.divider()

    # Section 4: 4 Behavioral Personas (LAK26 Clusters)
    st.markdown("### 4. Distribusi 4 Persona Perilaku (Adopsi LAK26 K-Means)")
    st.markdown(
        """
        Makalah McNichols et al. (2026) membagi mahasiswa ke dalam 4 klaster perilaku. 
        Tabel berikut memperlihatkan distribusi anggota klaster pada kohort riset beserta rata-rata nilai ujian mandiri:
        """
    )

    cluster_names = {
        0: "Cluster 0: Code Writers (Dominan Minta Sintesis Kode)",
        1: "Cluster 1: Coding Question Askers (Dominan Pertanyaan Konseptual)",
        2: "Cluster 2: General Question Askers (Campuran Konsep & Konteks)",
        3: "Cluster 3: Report Writers (Dominan Tulis Laporan & Konversi)",
    }

    if "cluster_k3" in df.columns:
        c_summary = []
        for c_id, name in cluster_names.items():
            sub = df[df["cluster_k3"] == c_id]
            if len(sub) > 0:
                c_summary.append({
                    "Klaster / Persona Perilaku": name,
                    "Jumlah Mahasiswa": len(sub),
                    "Persentase": f"{100*len(sub)/len(df):.1f}%",
                    "Rata-rata Nilai Ujian": f"{sub['no_llm_score'].mean()*100:.1f}%",
                    "Proporsi At-Risk": f"{100*(sub['at_risk']==1).mean():.1f}%",
                    "Karakteristik Kognitif": "Tingkat pemahaman konsep tertinggi" if c_id == 1 else (
                        "Risiko kegagalan tertinggi akibat circumvention" if c_id == 3 else "Keterlibatan moderat"
                    )
                })
        st.dataframe(pd.DataFrame(c_summary), width="stretch", hide_index=True)


if __name__ == "__main__":
    render()
