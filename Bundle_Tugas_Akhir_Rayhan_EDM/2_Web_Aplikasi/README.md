# Educational Data Mining (EDM) Early-Warning Testbed
**Predictive Modeling of Academic At-Risk Students from Chatbot Dialogue Dynamics**

- **Peneliti / Mahasiswa:** Muhammad Rayhan Najib (NIM: 240533600012)
- **Mata Kuliah:** Data Mining & Data Science
- **Dataset Acuan:** The StudyChat Dataset (LAK 2026 / arXiv:2503.07928)
- **Lisensi Data:** Creative Commons Attribution 4.0 International (CC BY 4.0)

---

## 1. Latar Belakang & Kebaruan Riset (*Research Novelty*)

Penelitian ini membedakan diri secara ilmiah dari paper primer terdahulu (*McNichols, Ikram, & Lan, LAK 2026*):
1. **Pergeseran Paradigma Masalah**: Paper LAK 2026 melakukan analisis korelasi regresi linier post-hoc deskriptif pasca-semester. Penelitian ini mengembangkan **Sistem Deteksi Dini Prospektif (*Early-Warning System*)** menggunakan klasifikasi terawasi multi-model.
2. **Definisi Target Valid**: Menetapkan target biner `at_risk = 1` berdasarkan performa ujian mandiri tanpa bantuan AI (`no_llm_score < 0.85`), mencakup 36.0% populasi kohort ($N=175$).
3. **Isolasi Kebocoran Data (*Zero-Leakage Guarantee*)**: Mengeluarkan seluruh variabel nilai akhir (`no_llm_score`, `llm_score`, `overall_score`, `cluster_k3`) dari matriks fitur masukan ($X$).
4. **Rekayasa Fitur Kognitif**: Memformulasikan 3 indikator komposit:
   - *Cognitive Independence Index*: Rasio pertanyaan konseptual terhadap permintaan pembuatan kode langsung.
   - *Troubleshooting Persistence*: Mengukur intensitas terjebak dalam lingkaran perulangan pesan error.
   - *Early Engagement Proactivity*: Persentase keaktifan tugas awal sebelum ujian berlangsung.

---

## 2. Cara Menjalankan Sistem (*Quick Start*)

Sesuai arahan dosen, sistem dapat dijalankan dengan **satu perintah utama**:

```bash
python app.py
```

Perintah di atas akan secara otomatis:
1. Menyiapkan runtime dan memuat dependensi pipeline.
2. Menjalankan server Streamlit pada port lokal `8501`.
3. Membuka peramban (*web browser*) secara otomatis dan mengakses `http://localhost:8501`.

*Alternatif Windows:* Klik ganda berkas `run.bat`.

---

## 3. Struktur Modul Proyek

```text
Data Science/
├── app.py                 # Entry point utama (auto-launch Streamlit & browser)
├── requirements.txt       # Dependensi pustaka terverifikasi
├── run.bat                # Peluncur praktis
├── README.md              # Laporan ilmiah, panduan demo, & FAQ dosen
├── .streamlit/
│   └── config.toml        # Tema resmi Academic Light Indigo
├── core/
│   ├── config.py          # Konstanta, token desain, & metadata
│   ├── data.py            # Ingestion dataset, caching, & audit kebocoran
│   ├── codebook.py        # Kamus data ilmiah & taksonomi fitur
│   ├── modeling.py        # Pipeline Imblearn/Sklearn, CV, & leaderboard
│   └── ui.py              # Visualisasi Plotly & komponen CSS terarah
├── views/
│   ├── 1_overview.py      # Executive Summary & Kamus Data
│   ├── 2_exploration.py   # Eksplorasi Fenomena Illusion of Competence
│   ├── 3_preparation.py   # Preparasi Data & Pratinjau Scaling
│   ├── 4_modelling.py     # Arena Tolok Ukur 8 Model & Skenario Waktu
│   ├── 5_evaluation.py    # Diagnostik Matriks Konfusi & Kurva ROC/PR
│   ├── 6_prediction.py    # Simulator Inferensi Risiko Dini Interaktif
│   └── 7_recommendations.py # Panduan Intervensi Pedagogis bagi Dosen
└── data/
    └── raw/
        └── studychat_cohort.json # Salinan data mentah tak tersentuh
```

---

## 4. Panduan Demo untuk Dosen (*Live Demo Script - 8 Langkah*)

Ikuti alur demonstrasi 8 langkah ini untuk presentasi yang kuat dan meyakinkan di depan dosen penguji:

1. **Jalankan Terminal:** Eksekusi `python app.py`. Tunjukkan bahwa aplikasi otomatis memicu Streamlit dan membuka browser ke `http://localhost:8501` tanpa kendala.
2. **Buka Halaman 1 (Executive Overview):** 
   - Tunjukkan kartu metrik kohort: 175 mahasiswa riil, 16.851 tuturan chat, 36.0% At-Risk.
   - Sorot tabel *Research Novelty*: jelaskan mengapa riset kita berbeda dari regresi LAK 2026.
3. **Buka Halaman 2 (Dinamika Dialog & Gap):**
   - Tunjukkan grafik *Illusion of Competence*: jelaskan bagaimana nilai tugas dengan AI (rata-rata 94.8%) mengalami disparitas tajam dengan nilai ujian mandiri (rata-rata 86.3%).
   - Tunjukkan tabel Welch's t-test: buktikan bahwa rasio konseptual dan rasio error memiliki perbedaan signifikan secara statistik ($p < 0.05$).
4. **Buka Halaman 3 (Preparasi & Zero Leakage):**
   - Tunjukkan tabel *Zero-Leakage Audit*: buktikan ke dosen bahwa tidak ada nilai masa depan (`no_llm_score`) yang bocor ke dalam data pelatihan.
   - Jelaskan 3 fitur rekayasa kognitif yang baru kita tambahkan.
5. **Buka Halaman 4 (Arena Model & Leaderboard):**
   - Tekan tombol **Latih Seluruh Model Sekarang**.
   - Tunjukkan hasil cross-validation 5-fold: model Random Forest dan Logistic Regression mengungguli baseline mayoritas secara signifikan pada metrik F1-Macro dan Recall At-Risk.
   - Alihkan skenario ke **Early Warning (Awal Semester)** untuk mendemonstrasikan bahwa data tugas awal A1–A3 sudah memiliki daya prediktif yang kuat.
6. **Buka Halaman 5 (Diagnostik & Eksplanabilitas):**
   - Tunjukkan Confusion Matrix ternormalisasi: perlihatkan tingkat False Alarm yang rendah.
   - Perlihatkan grafik *Permutation Feature Importance*: buktikan bahwa *Cognitive Independence* dan *Error Persistence* adalah fitur paling menentukan.
7. **Buka Halaman 6 (Simulasi Inferensi Risiko):**
   - Klik preset **"Profil B: Mahasiswa Terjebak Error"** -> Tunjukkan output inferensi otomatis: model mendeteksi status **ACADEMIC AT-RISK** dengan probabilitas tinggi.
   - Klik preset **"Profil A: Mahasiswa Mandiri"** -> Tunjukkan perubahan status menjadi **GOOD STANDING**.
8. **Buka Halaman 7 (Panduan Intervensi Dosen):**
   - Akhiri demo dengan memperlihatkan rekomendasi tindakan nyata bagi pengajar untuk membina mahasiswa, bukan sekadar melarang penggunaan AI.

---

## 5. Tanya Jawab Kunci Ujian Dosen (*Anticipated Lecturer Q&A*)

**Q1: Mengapa menggunakan metrik F1-Macro dan Balanced Accuracy, bukan Akurasi biasa?**  
> *Jawaban:* Distribusi kelas bersifat tidak seimbang (36% At-Risk vs 64% Good Standing). Akurasi biasa dapat dimanipulasi dengan menebak mayoritas saja. F1-Macro memberikan bobot setara pada kelas minoritas berisiko, sedangkan Recall At-Risk memastikan sesedikit mungkin mahasiswa rentan yang luput dari pendampingan.

**Q2: Mengapa memilih `class_weight='balanced'` dibandingkan SMOTE sebagai metode default?**  
> *Jawaban:* Pada sampel berukuran kecil hingga moderat ($N=175$), pembobotan loss function (`class_weight='balanced'`) mempenalti kesalahan pada kelas minoritas tanpa memanipulasi ruang sampel dengan data sintetis k-nearest neighbors yang rentan menghasilkan over-generalisasi di batas keputusan (*decision boundary*).

**Q3: Bagaimana Anda memastikan tidak ada kebocoran data (*Data Leakage*)?**  
> *Jawaban:* Pertama, seluruh preprocessing dan scaling dibungkus di dalam `Pipeline` sehingga parameter $\mu$ dan $\sigma$ hanya dipelajari dari lipatan pelatihan (*training folds*). Kedua, variabel nilai ujian mandiri (`no_llm_score`) dan nilai tugas (`llm_score`) secara ketat diisolasi dari matriks fitur $X$.

**Q4: Apa makna dari fitur rekayasa *Cognitive Independence Index*?**  
> *Jawaban:* Fitur ini membagi proporsi pertanyaan konsep dengan proporsi permintaan kode langsung. Nilai tinggi menandakan mahasiswa menggunakan AI sebagai mitra dialog pemahaman materi, sedangkan nilai rendah menandakan mahasiswa memperlakukan AI sebagai mesin pembuat tugas tanpa proses refleksi kognitif.

**Q5: Apa keterbatasan utama penelitian ini?**  
> *Jawaban:* Data berasal dari satu mata kuliah tingkat lanjut ilmu komputer (COMPSCI 383 UMass Amherst) dengan model gpt-4o-mini. Generalisasi ke mata kuliah non-teknis atau tingkat pemula memerlukan kalibrasi taksonomi dialog lebih lanjut.

---

## 6. Sitasi Formal

```bibtex
@inproceedings{mcnichols2026studychat,
  title={The StudyChat Dataset: Analyzing Student Dialogues With ChatGPT in an Artificial Intelligence Course},
  author={McNichols, Hunter and Ikram, Fareya and Lan, Andrew},
  booktitle={Proceedings of the 16th International Learning Analytics and Knowledge Conference (LAK 2026)},
  pages={53--63},
  year={2026},
  doi={10.1145/3785022.3785029}
}
```
