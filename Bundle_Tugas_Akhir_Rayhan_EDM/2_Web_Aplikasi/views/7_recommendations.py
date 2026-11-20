# -*- coding: utf-8 -*-
"""
views/7_recommendations.py
Actionable Pedagogical Intervention Guidelines for Course Instructors and Academic Advisors.
"""
import streamlit as st
import pandas as pd


def render() -> None:
    st.title("Rekomendasi Intervensi Pedagogis (*Actionable Guidelines*)")
    st.caption("Panduan berbasis bukti empiris untuk dosen dan pembimbing akademik dalam mengelola penggunaan LLM")

    st.markdown(
        """
        Berdasarkan temuan empiris makalah LAK 2026 dan hasil inferensi model prediktif kita, 
        dosen tidak perlu melarang penggunaan ChatGPT, melainkan **mengarahkan taksonomi dialog** mahasiswa.
        Berikut adalah 4 panduan intervensi terarah:
        """
    )

    # Strategy 1
    st.markdown("### 1. Mahasiswa Tipe 'Circumvention Report-Writer' (Risiko Tertinggi)")
    st.markdown(
        """
        - **Karakteristik Dialog:** Dominan menggunakan perintah <code>Writing Request: Write English</code> dan <code>Code/Data Conversion</code> untuk menyusun laporan tugas.
        - **Dampak Pembelajaran:** Mengalami penurunan skor ujian mandiri paling parah (rata-rata 83.8% dengan varians tinggi), karena tidak mengalami proses kognitif saat merangkum hasil.
        - **Tindakan Intervensi Dosen:**
          1. Wajibkan sesi *code defense* atau tanya jawab lisan singkat 3 menit untuk memvalidasi apakah mahasiswa benar-benar memahami narasi yang ditulis.
          2. Ubah bobot rubrik: kurangi porsi penilaian pada teks laporan statis dan perbesar porsi ujian mandiri tanpa AI.
        """
    )

    st.divider()

    # Strategy 2
    st.markdown("### 2. Mahasiswa Tipe 'Error Message Looper' (Indikator Kebingungan)")
    st.markdown(
        """
        - **Karakteristik Dialog:** Berulang kali menyalin pesan error terminal (<code>Provide Context: Error Message</code>) dan menanyakan klarifikasi spesifik (<code>Contextual Questions</code>) tanpa bertanya konsep dasar.
        - **Dampak Pembelajaran:** Terjebak dalam perulangan *trial-and-error* membabi-buta, berkorelasi negatif dengan capaian belajar.
        - **Tindakan Intervensi Dosen:**
          1. Berikan modul bimbingan *Systematic Debugging*: ajarkan cara membaca *stack trace* dan memeriksa nilai variabel secara mandiri sebelum menanyakannya ke AI.
          2. Fasilitasi sesi *Office Hours* terarah untuk mahasiswa yang terdeteksi memiliki `error_persistence_index > 5.0`.
        """
    )

    st.divider()

    # Strategy 3
    st.markdown("### 3. Jebakan Pertanyaan Matematika & Derivasi Rumus (*Math Pitfall*)")
    st.markdown(
        """
        - **Karakteristik Dialog:** Mengandalkan LLM untuk menurunkan persamaan matematis (misal: probabilitas tabel n-gram pada Tugas A6).
        - **Dampak Pembelajaran:** Berkorelasi negatif signifikan ($p = 0.002, \text{coef} = -0.106$) karena LLM sering berhalusinasi pada derivasi rumus formal.
        - **Tindakan Intervensi Dosen:**
          1. Berikan peringatan eksplisit di awal perkuliahan bahwa LLM tidak dapat diandalkan untuk pembuktian atau penurunan rumus matematis algoritmik.
          2. Sediakan kunci konsep matematika resmi di sistem manajemen pembelajaran (LMS).
        """
    )

    st.divider()

    # Strategy 4
    st.markdown("### 4. Pembinaan Mahasiswa Tipe 'Conceptual Inquirer' (Praktik Terbaik)")
    st.markdown(
        """
        - **Karakteristik Dialog:** Dominan menanyakan cara kerja library Python, struktur data, dan konsep Computer Science.
        - **Dampak Pembelajaran:** Memiliki skor ujian mandiri tertinggi ($89.0 \pm 7.3$) dan ketahanan konseptual yang kokoh.
        - **Tindakan Intervensi Dosen:**
          1. Dorong mahasiswa untuk terus menggunakan LLM sebagai *Socratic Tutor* (tutor dialogis).
          2. Libatkan mahasiswa dari kelompok ini sebagai *peer tutor* atau fasilitator diskusi kelompok di kelas laboratorium.
        """
    )

    st.divider()

    # Summary Checklist Table
    st.markdown("### Checklist Kebijakan Kelas (*AI Classroom Policy Checklist*)")
    chk_df = pd.DataFrame([
        {"Tahap Evaluasi": "Minggu 1-4 (Tugas A1-A3)", "Aksi Pengajar": "Pantau indikator Early Engagement Share. Identifikasi mahasiswa pasif sebelum Ujian 1."},
        {"Tahap Evaluasi": "Minggu 5-8 (Tugas A4-A5)", "Aksi Pengajar": "Periksa rasio Cognitive Independence. Panggil mahasiswa yang terindikasi 100% bergantung pada sintesis kode."},
        {"Tahap Evaluasi": "Minggu 9-12 (Tugas A6-A7)", "Aksi Pengajar": "Beri peringatan bahaya halusinasi rumus matematis n-gram. Berikan pendampingan intensif."},
        {"Tahap Evaluasi": "Persiapan Ujian Akhir", "Aksi Pengajar": "Jalankan simulasi risiko untuk seluruh kohort untuk menentukan mahasiswa yang butuh sesi remedial."}
    ])
    st.dataframe(chk_df, width="stretch", hide_index=True)


if __name__ == "__main__":
    render()
