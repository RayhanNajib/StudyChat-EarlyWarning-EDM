# -*- coding: utf-8 -*-
"""
views/1_overview.py
Executive Overview, Research Foundations, Citation, and Interactive Data Dictionary.
"""
import streamlit as st
import pandas as pd

from core.config import (
    PROJECT_TITLE,
    PROJECT_SUBTITLE,
    STUDENT_NAME,
    STUDENT_NIM,
    CITATION_APA,
    CITATION_BIBTEX,
    DATASET_LICENSE,
)
from core.data import load_cohort_dataframe, get_cohort_summary_stats
from core.codebook import get_data_dictionary
from core.ui import render_metric_card


def render() -> None:
    st.title("Executive Overview & Landasan Riset")
    st.caption(f"{PROJECT_TITLE} — {PROJECT_SUBTITLE}")

    # Author & Academic Metadata
    st.markdown(
        f"""
        <div class="alert-box alert-info">
            <strong>Peneliti / Mahasiswa:</strong> {STUDENT_NAME} (NIM: {STUDENT_NIM})<br>
            <strong>Topik Tugas Akhir:</strong> Educational Data Mining & Early-Warning Predictive System<br>
            <strong>Status Target:</strong> <code>no_llm_score &lt; 0.85</code> (Deteksi Mahasiswa Berisiko Akademik pada Ujian Tanpa AI)
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_cohort_dataframe()
    stats = get_cohort_summary_stats(df)

    # Key Cohort Metrics
    st.markdown("### Ringkasan Kohort Riset (StudyChat Benchmark)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Ukuran Kohort Mahasiswa", f"{stats['total_students']} Siswa", "Sampel riil persetujuan etik", status="primary")
    with c2:
        render_metric_card("Mahasiswa At-Risk (Target)", f"{stats['at_risk_count']} ({stats['at_risk_percentage']}%)", "no_llm_score < 0.85", status="at_risk")
    with c3:
        render_metric_card("Good Standing", f"{stats['good_standing_count']} ({100 - stats['at_risk_percentage']:.1f}%)", "no_llm_score >= 0.85", status="safe")
    with c4:
        render_metric_card("Total Tuturan Dialog", f"{stats['total_dialogue_turns']:,}", "Interaksi 7 tugas pemrograman", status="normal")

    st.divider()

    # Research Distinction: Prior Paper vs Our Project
    st.markdown("### Kebaruan Riset (*Research Novelty*) vs Paper Terdahulu")
    st.markdown(
        """
        Penelitian ini berakar pada dataset publik **StudyChat** (McNichols, Ikram, & Lan, *LAK 2026*), 
        namun memiliki rumusan masalah, metodologi, dan tujuan aplikatif yang **berbeda secara fundamental**:
        """
    )
    
    comp_df = pd.DataFrame([
        {
            "Dimensi Analisis": "Fokus Utama Masalah",
            "Paper McNichols et al. (LAK 2026)": "Deskriptif pasca-semester: observasi korelasi tuturan & validasi dataset.",
            "Sistem Deteksi Dini Kita (Tugas Akhir)": "Preskriptif & Prediktif: Deteksi dini mahasiswa berisiko gagal sebelum ujian mandiri."
        },
        {
            "Dimensi Analisis": "Tipe Pemodelan",
            "Paper McNichols et al. (LAK 2026)": "Regresi linier kontinu (penulis mengakui model rentan overfitting & daya jelas rendah).",
            "Sistem Deteksi Dini Kita (Tugas Akhir)": "Klasifikasi terawasi multi-model (Ensemble, SVM, Tree) dengan penanganan imbalance."
        },
        {
            "Dimensi Analisis": "Waktu Prediksi",
            "Paper McNichols et al. (LAK 2026)": "Retrospektif: Menghitung total tuturan setelah seluruh semester selesai.",
            "Sistem Deteksi Dini Kita (Tugas Akhir)": "Prospektif (Early-Warning): Menguji kemampuan prediksi interaksi awal (A1-A3)."
        },
        {
            "Dimensi Analisis": "Isolasi Kebocoran Data",
            "Paper McNichols et al. (LAK 2026)": "Memasukkan rata-rata nilai sebelumnya sebagai prediktor utama.",
            "Sistem Deteksi Dini Kita (Tugas Akhir)": "Isolasi 100% (Zero Leakage): Murni menguji dinamika kognitif tuturan dialog."
        },
        {
            "Dimensi Analisis": "Luaran Produk",
            "Paper McNichols et al. (LAK 2026)": "Artikel prosiding konferensi statis (PDF).",
            "Sistem Deteksi Dini Kita (Tugas Akhir)": "Dashboard interaktif lokal (Streamlit) dengan inferensi real-time."
        }
    ])
    st.dataframe(comp_df, width="stretch", hide_index=True)

    st.divider()

    # Interactive Data Dictionary
    st.markdown("### Kamus Data Ilmiah (*Data Dictionary & Codebook*)")
    st.caption("Pemeriksaan tipe data, peran dalam pipeline, dan verifikasi status isolasi kebocoran target:")
    codebook_df = get_data_dictionary()
    st.dataframe(codebook_df, width="stretch", hide_index=True)

    st.divider()

    # Academic Citation & License
    st.markdown("### Sitasi Ilmiah & Lisensi Dataset")
    st.markdown(f"**Lisensi Dataset:** {DATASET_LICENSE}")
    st.markdown(f"**Sitasi Format APA:**\n> *{CITATION_APA}*")
    with st.expander("Lihat Entri BibTeX"):
        st.code(CITATION_BIBTEX, language="bibtex")


if __name__ == "__main__":
    render()
