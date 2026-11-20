# Rangkuman & Penjelasan Lengkap Materi: Data Mining 1 - Introduction

**Dosen / Penyusun:** Utomo Pujianto (Universitas Negeri Malang)  
**Mata Kuliah:** Data Science / Data Mining  
**File Acuan:** [Data Mining 1 - Introduction.pdf](file:///C:/Users/WA/Downloads/TUGAS%20PKKMB/Data%20Science/Data%20Mining%201%20-%20Introduction.pdf)

---

## 📌 Pengantar Singkat (Mengapa Kita Butuh Data Mining?)

Materi ini menjelaskan dasar-dasar **Data Mining** dari tingkat pemula sampai pemahaman metodologi kerja industri.

Saat ini dunia mengalami ledakan data (*data explosion*) dari media sosial, sensor, transaksi bisnis, hingga sistem digital. Namun, **banyaknya data tidak otomatis membuat kita bijak**. 

> 💬 *"We are drowning in data, but starving for knowledge!"* (John Naisbitt)  
> *(Kita tenggelam dalam lautan data, tetapi kelaparan akan pengetahuan!)*

> 💬 *"Those who rule data will rule the entire world."* (Masayoshi Son)  
> *(Siapa yang menguasai data, dia yang akan menguasai seluruh dunia).*

---

## 🧠 1. Hierarki DIKW (Data $\rightarrow$ Information $\rightarrow$ Knowledge $\rightarrow$ Wisdom)

Untuk memahami posisi Data Mining, kita harus paham piramida DIKW:

```text
       ▲
      / \        [Wisdom]       -> Keputusan Strategis / Kebijakan
     /   \
    /     \      [Knowledge]    -> Pola / Wawasan Tersembunyi (Hasil Data Mining)
   /       \
  /         \    [Information]  -> Data Terstruktur + Konteks
 /           \
/_____________\  [Data]         -> Fakta Mentah / Angka Tanpa Konteks
```

* **Data**: Angka atau fakta mentah. Contoh: `28, 30, 29`.
* **Information**: Data yang diberi konteks sehingga bermakna. Contoh: `Suhu udara kota Malang dalam 3 hari terakhir adalah 28°C, 30°C, 29°C`.
* **Knowledge (Pengetahuan)**: Pola atau wawasan yang didapat dari analisis informasi. Contoh: `Suhu udara meningkat saat musim kemarau dan menyebabkan konsumsi listrik AC naik 20%`. *(Di sinilah peran Data Mining!)*
* **Wisdom (Kebijaksanaan)**: Keputusan aksi berdasarkan pengetahuan. Contoh: `PLN menambah cadangan daya listrik di musim kemarau`.

---

## 💡 2. Apakah Itu Data Mining?

**Definisi Data Mining:**  
Proses ekstraksi atau penemuan **pola yang tersembunyi, belum diketahui sebelumnya, valid, dan berharga (*actionable knowledge*)** dari sekumpulan data yang berukuran sangat besar (*Big Data*).

### 🔍 Hubungan Data Science, Data Mining, dan Machine Learning
* **Data Science**: Bidang payung (*umbrella field*) yang sangat luas meliputi statistik, analitis, Machine Learning, dan Data Mining.
* **Data Mining**: Proses spesifik menemukan pola dari dataset besar.
* **Machine Learning**: Algoritma yang dilatih (*trained*) menggunakan data agar komputer bisa belajar dan memprediksi secara otomatis.

---

## 🛠️ 3. Tugas-Tugas Data Mining (Data Mining Tasks)

Tugas Data Mining dibagi menjadi 2 kategori utama: **Predictive (Supervised)** dan **Descriptive (Unsupervised)**.

```text
                        ┌────────────────────────────────────────┐
                        │           DATA MINING TASKS            │
                        └───────────────────┬────────────────────┘
                                            │
           ┌────────────────────────────────┴────────────────────────────────┐
           ▼                                                                 ▼
┌─────────────────────────┐                                      ┌─────────────────────────┐
│       PREDICTIVE        │                                      │       DESCRIPTIVE       │
│   (Supervised Learning) │                                      │  (Unsupervised Learning)│
└──────────┬──────────────┘                                      └──────────┬──────────────┘
           │                                                                │
           ├─► Classification (Nominal)                                     ├─► Clustering (Pengelompokan)
           ├─► Regression (Numerik/Kontinu)                                 ├─► Anomaly / Outlier Detection
           └─► Time Series Forecasting                                      ├─► Association Rule Mining
                                                                            └─► Sequential & Link Analysis
```

### 🅰️ Predictive (Supervised Learning — Ada Label Target)
Supervised learning menggunakan data latih yang **sudah memiliki label/kunci jawaban**.

1. **Classification (Klasifikasi):**
   * **Tujuan**: Memprediksi kategori/kelas nominal dari data baru.
   * **Contoh**: Memprediksi email (*Spam* / *Bukan Spam*), memprediksi kredit (*Layak* / *Macet*).
   * **Algoritma Populer**: *k-Nearest Neighbors (k-NN), Naive Bayes, Decision Tree, Random Forest, Support Vector Machine (SVM)*.
2. **Regression / Estimation (Regresi):**
   * **Tujuan**: Memprediksi nilai numerik kontinu.
   * **Contoh**: Memprediksi harga rumah berdasarkan luas tanah, memprediksi estimasi gaji.
   * **Algoritma Populer**: *Simple Linear Regression, Multiple Linear Regression*.
3. **Time Series Forecasting:**
   * **Tujuan**: Memprediksi nilai di masa depan berdasarkan tren urutan waktu.
   * **Contoh**: Prediksi harga saham besok, prediksi cuaca minggu depan.

---

### 🅱️ Descriptive (Unsupervised Learning — Tanpa Label Target)
Unsupervised learning mencari pola alami dalam data **tanpa arahan label target**.

1. **Cluster Analysis (Clustering / Pengelompokan):**
   * **Tujuan**: Mengelompokkan objek-objek data yang mirip ke dalam satu kelompok (*cluster*) berdasarkan kedekatan jarak.
   * **Contoh**: Segmentasi pelanggan minimarket berdasarkan kebiasaan belanja.
   * **Algoritma Populer**: *K-Means, DBSCAN, Hierarchical Clustering*.
2. **Anomaly / Outlier Detection (Deteksi Anomali):**
   * **Tujuan**: Mendeteksi data liar/aneh yang jauh berbeda dari pola umum.
   * **Contoh**: Deteksi kecurangan transaksi kartu kredit (*fraud detection*), deteksi kerusakan mesin pabrik.
3. **Co-occurrence Pattern Mining (Association Rule Mining / Market Basket Analysis):**
   * **Tujuan**: Menemukan barang-barang yang sering dibeli bersamaan.
   * **Contoh**: *"Jika pembeli membeli Roti dan Mentega, maka 80% kemungkinan mereka juga membeli Susu"*.
   * **Algoritma Populer**: *Apriori, FP-Growth*.
4. **Sequential Pattern Mining & Link Analysis:**
   * **Tujuan**: Menemukan urutan kejadian yang berulang seiring waktu atau menganalisis hubungan graf antar akun/halaman web (misal algoritma *PageRank* Google).

---

## 🔄 4. Metodologi Standar Industri: CRISP-DM

**CRISP-DM** (*Cross-Industry Standard Process for Data Mining*) adalah standar alur kerja 6 tahap yang digunakan para ilmuwan data di industri:

```text
┌────────────────────────┐      ┌────────────────────────┐
│ 1. Business            │ ◄──► │ 2. Data                │
│    Understanding       │      │    Understanding       │
└───────────┬────────────┘      └───────────┬────────────┘
            │                               │
            ▼                               ▼
┌────────────────────────┐      ┌────────────────────────┐
│ 6. Deployment          │ ◄──┐ │ 3. Data                │
└────────────────────────┘    │ │    Preparation         │
            ▲                 │ └───────────┬────────────┘
            │                 │             │
┌───────────┴────────────┐    │             ▼
│ 5. Evaluation          │ ◄──┴─── 4. Modeling           │
└────────────────────────┘                               
```

### 6 Tahapan CRISP-DM:
1. **Business Understanding (Pemahaman Bisnis)**:  
   Menentukan tujuan bisnis, mendefinisikan masalah, dan mengubahnya menjadi tujuan teknik data mining.
2. **Data Understanding (Pemahaman Data)**:  
   Mengumpulkan data awal, mengamati struktur data, mengecek kualitas data, dan menemukan wawasan pertama.
3. **Data Preparation (Persiapan & Pembersihan Data)**:  
   Menyeleksi, membersihkan data mentah (*data cleaning*), mengatasi nilai hilang (*missing values*), dan merubah format data agar siap dimasukkan ke model *(Memakan waktu hingga 80% total pengerjaan!)*.
4. **Modeling (Pemodelan)**:  
   Memilih dan menerapkan algoritma Data Mining (seperti *Decision Tree* atau *K-Means*) dan menyetel parameter terbaik.
5. **Evaluation (Evaluasi Model)**:  
   Menilai apakah akurasi dan kinerja model sudah memenuhi tujuan bisnis yang ditetapkan di tahap awal.
6. **Deployment (Penerapan)**:  
   Mengintegrasikan model yang sudah jadi ke dalam aplikasi/sistem bisnis operasional agar bisa digunakan oleh pengguna.

---

## 📜 5. 9 Hukum Data Mining (*Nine Laws of Data Mining* oleh Tom Khabaza)

Tom Khabaza merumuskan 9 aturan emas dalam proyek Data Mining:

| No | Nama Hukum | Inti / Penjelasan Singkat | Contoh Nyata / Implementasi |
| :-: | :--- | :--- | :--- |
| **1** | **Business Goals Law** | Proyek data mining harus selalu dimulai dari tujuan bisnis yang jelas. | Target memprediksi kehamilan pelanggan minimarket untuk penawaran popok bayi. |
| **2** | **Business Knowledge Law** | Pengetahuan bisnis sangat krusial untuk menafsirkan data. | Pakar perbankan memahami arti kode transaksi mencurigakan. |
| **3** | **Data Preparation Law** | Persiapan data mengambil porsi terbesar (sekitar 80% kerja). | Membersihkan teks, menghapus duplikat, merapikan format data. |
| **4** | **No Free Lunch Theorem (NFL-DM)** | Tidak ada satu algoritma yang paling sempurna untuk semua masalah. | Algoritma *Decision Tree* bagus di dataset A, tetapi *SVM* lebih unggul di dataset B. |
| **5** | **Right Tool Law** | Gunakan alat yang sesuai dengan masalah, bukan memaksakan 1 alat saja. | Memilih Python/R atau RapidMiner sesuai skala data. |
| **6** | **Insight Law** | Data mining harus menghasilkan wawasan yang dapat ditindaklanjuti. | Menata ulang tata letak barang minimarket berdasarkan hasil analisis asosiasi. |
| **7** | **Prediction Law** | Prediksi meningkatkan nilai informasi secara lokal melalui generalisasi. | Memprediksi risiko gagal bayar pinjaman nasabah baru. |
| **8** | **Value Law** | Nilai proyek ditentukan dari hasil keberhasilan bisnis, bukan rumitnya algoritma. | Algoritma sederhana yang menaikkan omzet 20% lebih bernilai dibanding algoritma rumit yang tidak terpakai. |
| **9** | **Deployment Law** | Data mining baru bermanfaat jika hasil model di-deploy ke sistem bisnis. | Memasang model deteksi spam langsung ke server email. |

---

## 🎯 Kesimpulan Ringkas Untuk Diingat:

1. **Data Mining** adalah proses mencari "emas" (pengetahuan/pola tersembunyi) di dalam "gunung sampah" (Big Data).
2. **Kategori Tugas**:
   * **Supervised (Klasifikasi/Regresi)**: Ada target/jawaban yang dilatih.
   * **Unsupervised (Clustering/Asosiasi)**: Tidak ada target, mencari kelompok/pola alami.
3. **CRISP-DM**: Siklus kerja 6 tahap standar industri *(Business Understanding $\rightarrow$ Data Understanding $\rightarrow$ Data Prep $\rightarrow$ Modeling $\rightarrow$ Evaluation $\rightarrow$ Deployment)*.
4. **Prinsip Utama**: Selalu utamakan **Tujuan Bisnis (*Business Goals First*)**, karena kecanggihan algoritma tidak ada artinya jika tidak menyelesaikan masalah dunia nyata.
