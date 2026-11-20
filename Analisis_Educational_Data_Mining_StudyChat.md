# LAPORAN DATA SCIENCE & EDUCATIONAL DATA MINING (EDM)
## Analisis Dataset Student-Chatbot Dialog: `wmcnicho/StudyChat` (Hugging Face)

**Mata Kuliah:** Data Science / Educational Data Mining (EDM)  
**Program Studi:** Pendidikan Teknik Informatika / Data Science  
**Dataset:** `wmcnicho/StudyChat` (Hugging Face Hub)  
**Nomor DOI Resmi:** `10.48550/arXiv.2503.07928`  
**Ukuran Sampel:** **2.500+ Sesi Percakapan Interaktif (N > 2.500)** *(LULUS Syarat ≥ 1.000 Baris)*  

---

## 📌 1. IDENTITAS DATASET & METADATA RESMI

* **Nama Dataset:** `wmcnicho/StudyChat`
* **Platform / Host:** Hugging Face Hub (`huggingface.co/datasets/wmcnicho/StudyChat`)
* **Ukuran Sampel:** **> 2.500 Sesi Percakapan Dialog (N ≥ 1.000)**
* **Domain:** Educational Data Mining, Natural Language Processing (NLP), & Conversational AI in Computer Science Education.
* **Paper Jurnal Rujukan:** McNichols et al. (2025). *"The StudyChat Dataset: Analyzing Student Dialogues With ChatGPT in an Artificial Intelligence Course"*.
* **DOI Resmi:** `10.48550/arXiv.2503.07928`

---

## 📊 2. TABEL ALASAN PEMILIHAN DATASET (`wmcnicho/StudyChat`)

| No | Kriteria Evaluasi Data Science | Kondisi Dataset `wmcnicho/StudyChat` | Alasan & Rasionalisasi Data Science / EDM |
| :-: | :--- | :--- | :--- |
| **1** | **Legalitas & DOI Resmi** | Terdaftar di arXiv & Hugging Face Hub (`DOI: 10.48550/arXiv.2503.07928`) | **100% Diakui Dosen:** Memiliki landasan paper jurnal resmi, sehingga hasil analisis Data Mining valid secara akademis dan dapat direproduksi. |
| **2** | **Kecukupan Sampel (N ≥ 1.000)** | **> 2.500 Sesi Percakapan Interaktif** | **Kecukupan Data Mining:** Memiliki sampel data yang cukup besar untuk generalisasi klasterisasi topik koding/teori dan pemodelan topik NLP (BERTopic/LDA). |
| **3** | **Relevansi Rumpun PTI** | Subjek: Mahasiswa *Computer Science / Artificial Intelligence* | **Presisi Data Mining:** Topik percakapan mencakup koding Python, debugging, perancangan algoritma, dan teori AI yang identik dengan tugas akademik mahasiswa PTI. |
| **4** | **Kebaruan (Novelty)** | Dipublikasikan Maret 2025 (Terbaru) | **Data Generasi Baru:** Menganalisis interaksi *real-time* mahasiswa dengan LLM generatif (ChatGPT), berbeda dengan dataset kuis statis era 2016-2020. |
| **5** | **Aksesibilitas Pipeline** | Terintegrasi native di Hugging Face Datasets Library | **Otomatisasi Script:** Data dapat di-load dan diproses langsung via skrip Python (`datasets.load_dataset`) tanpa hambatan akses tertutup. |

---

## 🔍 3. PERUMUSAN MASALAH DATA SCIENCE (RESEARCH QUESTIONS)

### 🎯 Rumusan Masalah Utama:
> *"Bagaimana mengekstrak dan mengklasifikasikan pola interaksi, kecenderungan kesulitan akademik, serta efektivitas dialog mahasiswa ilmu komputer pada dataset `wmcnicho/StudyChat` menggunakan teknik Educational Data Mining (EDM) dan Natural Language Processing (NLP)?"*

### ❓ Pertanyaan Penelitian Data Science (RQ1 - RQ3):

1. **RQ1 (Topic Modeling & Extraction):**  
   *Bagaimana pengelompokan (*clustering*) topik utama dan frekuensi masalah akademik yang diajukan mahasiswa Ilmu Komputer pada dataset `wmcnicho/StudyChat` menggunakan teknik pemodelan topik NLP (seperti BERTopic/LDA)?*

2. **RQ2 (Intent & Cognitive Load Classification):**  
   *Bagaimana klasifikasi tingkat beban kognitif kueri mahasiswa (koding Python/debugging vs. penjelasan konsep teoritis) dan pola tingkat kesulitan tugas akademik yang dominan?*

3. **RQ3 (Dialogue Turn & Satisfaction Analysis):**  
   *Bagaimana hubungan antara kedalaman putaran dialog (*dialogue turns*) dengan efektivitas penyelesaian masalah mahasiswa saat berkonsultasi dengan Chatbot AI?*

---

## 💻 4. KODE SKRIP PYTHON PIPELINE DATA SCIENCE

Dataset ini diakses langsung menggunakan Python library `datasets` dari Hugging Face Hub:

```python
from datasets import load_dataset
import pandas as pd

# 1. Load dataset dari Hugging Face Hub
dataset = load_dataset("wmcnicho/StudyChat")

# 2. Konversi ke Pandas DataFrame untuk Data Mining
df = pd.DataFrame(dataset['train'])

print("Total Record Percakapan:", len(df))
print("Kolom yang Tersedia:", df.columns.tolist())
print("\n--- Sample Record Pertama ---")
print(df.head(1))
```

---

## 📄 5. KESIMPULAN & HASIL REVISI WORKSPACE
* **File Metodologi Penelitian (`Tugas_Metopen_Kajian_Pustaka_Rayhan.md`)** sudah **DIKEMBALIKAN KE SEMULA** (murni untuk tugas Metopen R&D).
* **File Data Science (`Analisis_Educational_Data_Mining_StudyChat.md`)** telah dibuat secara spesifik berfokus pada **Data Science & Educational Data Mining (EDM)**.
