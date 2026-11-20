# PANDUAN MEMBACA DATASET STUDychat (arXiv:2503.07928)

> 

---

## 1. Dataset ini apa, singkatnya?

**StudyChat** = rekaman nyata percakapan mahasiswa dengan chatbot AI (mirip ChatGPT)
selama **satu semester penuh** di mata kuliah **Artificial Intelligence** tingkat universitas.

Peneliti (McNichols, Ikram, Lan — 2025) bikin aplikasi web yang meniru fungsi ChatGPT,
lalu mencatat **(log)** semua interaksi mahasiswa. Hasilnya **16.851 interaksi** yang
dianotasi (diberi label) memakai skema *dialogue act* (jenis aksi percakapan).

**Paper fokus ke satu pertanyaan besar:**
> Bagaimana cara mahasiswa pakai AI — dan apakah cara pakai itu berkorelasi dengan nilai akhir mereka?

**Temuan utama paper (2 poin penting):**
1. Mahasiswa yang pakai AI untuk **minta pemahaman konsep** dan **bantuan ngoding** → cenderung **nilainya lebih baik**.
2. Mahasiswa yang pakai AI untuk **menulis laporan / "nembak" jawaban** (menghindari tujuan belajar tugas) → **nilai ujiannya lebih rendah**.

Jadi inti penelitian = **korelasi antara perilaku bertanya vs hasil belajar**.

---

## 2. Isi folder dataset (folder per folder)

Dataset asli di Hugging Face (`wmcnicho/StudyChat`). Salinan lokal ada di folder `StudyChat_Full_Dataset/`.
Abaikan folder `.cache/` (itu cuma jejak unduhan, bukan data).

| Folder | Isi | Format | Jumlah |
|---|---|---|---|
| `dialogues/` | Percakapan yang sudah dilabeli | `.jsonl` (JSON per baris) | **2 file**, 16.851 baris total |
| `scores/` | Nilai mahasiswa (yang setuju membuka nilai) | `.csv` | **2 file**, 183 mahasiswa |
| `submissions/` | Kumpulan hasil pekerjaan mahasiswa (mentah) | `.zip` | 1 file |
| `assignment_text/` | Teks/petunjuk tugas (a1–a7) per semester | `.md`, `.py`, `.ipynb`, `.csv` | 67 file |

### 2a. `dialogues/` — jantung dataset

Dua file:
- `f24_labeled_dialogues.jsonl` → **Semester Fall 2024**, 6.864 interaksi.
- `s25_labeled_dialogues.jsonl` → **Semester Spring 2025**, 9.987 interaksi.

Total = **16.851 interaksi** (cocok persis dengan angka di judul paper).

Satu baris = satu giliran tanya-jawab. Kolom penting per baris:

| Field                                           | Arti                                                      |
| ----------------------------------------------- | --------------------------------------------------------- |
| `prompt`                                        | Teks pertanyaan mahasiswa                                 |
| `response`                                      | Jawaban chatbot                                           |
| `topic`                                         | Tugas mana (`a1`...`a7`)                                  |
| `messages`                                      | Riwayat percakapan penuh (system/user/assistant)          |
| `userId`, `chatId`                              | Identitas mahasiswa & sesi chat (anonim)                  |
| `interactionCount`, `chatTotalInteractionCount` | Hitungan giliran                                          |
| `chatTitle`                                     | Judul chat                                                |
| `timestamp`, `chatStartTime`                    | Waktu                                                     |
| `llm_label`                                     | **Label aksi percakapan** (isi `label` + `justification`) |

### 2b. `scores/` — nilai

- `f24_grades_released_normalized.csv` → 70 mahasiswa (F24).
- `s25_grades_released_normalized.csv` → 111 mahasiswa (S25).
- Kolom: `userId`, `directory_name`, lalu nilai `a1`–`a7` (tugas), `e1`,`e2`,`e3` (ujian),
  lalu agregat `llm` (rata-rata tugas, dibobot) dan `no_llm` (rata-rata ujian, dibobot).
- Semua nilai dinormalisasi (0–1). Ada nilai > 1 karena soal bonus.

> Catatan kejujuran penting: **bukan semua mahasiswa** ada nilainya — hanya yang setuju
> membuka nilai (183 dari keseluruhan). Itu sebabnya angka profil bisa beda-beda.

### 2c. `assignment_text/` — materi tugas

7 tugas (a1–a7) per semester, berisi soal + petunjuk. Ini konteks yang menentukan
*topik apa* yang sedang ditanyakan mahasiswa.

---

## 3. Skema label `llm_label` (dialogue act)

Setiap interaksi dilabeli ke **kategori > subkategori**. Contoh nilai `label`:

```
writing_request > Write Code          (minta tuliskan kode)
conceptual_questions > Python Library (tanya konsep library)
provide_context > Error Message       (memberi konteks pesan error)
contextual_questions > Code Explanation
verification > Verify Code
editing_request > Edit Code
off_topic > Greeting
```

**7 kategori induk** (dari distribusi data):
1. `writing_request` — minta AI menulis sesuatu (kode / teks).
2. `conceptual_questions` — tanya pemahaman konsep.
3. `contextual_questions` — tanya konteks / penjelasan kode / klarifikasi tugas.
4. `provide_context` — mahasiswa memberi konteks (kode / pesan error / info tugas).
5. `verification` — minta cek benar-salah.
6. `editing_request` — minta perbaikan (kode / teks).
7. `off_topic` / `misc` — di luar pembelajaran.

Label subkategori **paling sering muncul** (pola perilaku):

| Subkategori | Makna | Sebaran |
|---|---|---|
| `Write Code` | minta tulis kode utuh | ~2.500 (f24+s25) |
| `Python Library` | tanya cara pakai library | ~1.780 |
| `Write English` | minta tulis teks laporan | ~1.340 |
| `Error Message` | beri konteks pesan error | ~980 |
| `Programming Language` | tanya bahasa pemrograman | ~1.270 |

> Ini penting: label `Write English` / `Summarize` = perilaku "nulis laporan pakai AI",
> yang di paper justru berkorelasi dengan nilai **lebih rendah**.

---

## 4. Istilah yang dipakai di web kita

### K-Means Clustering (Klastering)

**Apa?** Algoritma mengelompokkan data jadi **k** kelompok (klaster) tanpa label
(*unsupervised learning*).

**Cara kerja (4 langkah):**
1. Tentukan jumlah kelompok **k** (misal k=3).
2. Pilih **k** titik pusat (centroid) awal.
3. Setiap data masuk ke **centroid terdekat** (jarak Euclidean).
4. Centroid digeser ke rata-rata anggotanya → ulangi langkah 3–4 sampai stabil.

**Tujuan di web kita:** menemukan **persona belajar** — tipe mahasiswa yang mirip
berdasarkan perilaku bertanya mereka.

### Normalisasi (Z-score / standardisasi)

Menyamakan skala fitur agar fitur bernilai besar (misal total giliran chat = ratusan)
tidak "mendominasi" fitur bernilai kecil (misal rasio 0–1).

```
z = (x - rata_rata) / simpangan_baku
```

### Outlier (pencilan) & IQR

**Outlier** = data yang menyimpang jauh dari mayoritas.
**IQR (Interquartile Range)** = selisih kuartil atas (Q3) dan bawah (Q1), ukuran sebaran.
Aturan deteksi: nilai di luar `Q1 − 1.5×IQR` dan `Q3 + 1.5×IQR` dianggap outlier.

### Classification (Klasifikasi)

Memprediksi **label diskret** (kategori) dari fitur — beda dengan regresi yang memprediksi
angka kontinu. Algoritma yang dipakai:

| Algoritma | Konsep sederhana |
|---|---|
| **Naive Bayes** | Hitung peluang label dari tiap fitur, asumsi fitur saling bebas |
| **k-NN** | Label ditentukan suara terbanyak dari **k** tetangga terdekat |
| **Logistic Regression** | Fungsi sigmoid memetakan fitur ke peluang 0–1 |
| **Random Forest** | Kumpulan banyak pohon keputusan, hasilnya voting |

### Confusion Matrix & ROC-AUC

- **Confusion Matrix** = tabel benar/salah prediksi (TP, FN, FP, TN) → dasar hitung akurasi, presisi, recall, F1.
- **ROC-AUC** = seberapa baik model membedakan kelas positif vs negatif (0.5 = tebak acak, 1.0 = sempurna).

---

## 5. Web kita itu apa, dan proses datanya gimana

**Web = "EDM Testbed"** — dashboard statis (HTML + JavaScript + Chart.js) yang
memperlihatkan **alur CRISP-DM** atas dataset StudyChat secara transparan.
Bukan model AI hidup; ia **memutar ulang hasil analisis yang sudah dihitung**.

**Alur pemrosesan (yang ditampilkan tab "Pipeline"):**

```
1. INPUT DATASET     → baca StudyChat (dialogues + scores)
2. PREPROCESSING     → ambil fitur perilaku per mahasiswa, bersihkan, gabungkan
3. DETEKSI OUTLIER   → deteksi IQR (1.5×IQR) per fitur
4. NORMALISASI       → Z-score, samakan skala
5. PEMODELAN         → (a) K-Means klastering persona; (b) klasifikasi risiko
6. EVALUASI          → confusion matrix, F1, ROC-AUC, elbow SSE
```

**Fitur perilaku** yang dihitung dari dialog per mahasiswa:
`total_turns` (banyak giliran), `avg_prompt_len` (panjang rata-rata pertanyaan),
`conceptual_ratio` (seberapa banyak tanya konsep), `write_code_ratio` (seberapa banyak
minta kode), `error_msg_ratio` (seberapa sering mengirim pesan error).

**Dua sisi analisis:**
1. **Unsupervised (K-Means)** → membagi mahasiswa jadi **3 persona**:
   - Cluster 0: *Exploratory Synthesizers* (aktif eksplorasi konsep)
   - Cluster 1: *Passive Scaffolders* (mengandalkan bantuan terstruktur)
   - Cluster 2: *Impulse-Prone Strugglers* (sering terjebak error, butuh pendampingan)
2. **Supervised (Classification)** → memprediksi **risiko akademik** (`at_risk` ya/tidak)
   dari fitur perilaku. Model terbaik: **k-NN** (F1-macro ~0.51, ROC-AUC ~0.53).

**Kenapa pakai model itu (bukan asal-asalan):**
- K-Means → tepat untuk menemukan pola kelompok **tanpa label** di data perilaku.
- Normalisasi dulu → fitur beda skala, wajib agar jarak centroid adil.
- Classifier 4 algoritma dibandingkan → biar terlihat proses seleksi, bukan klaim kosong.
- Naive Bayes dipakai sebagai **baseline** pembanding (sederhana, cepat, fair).

---

## 6. Batasan & kejujuran data

- **Jumlah bisa beda-beda** tergantung level agregasi: 16.851 = interaksi (level baris),
  183 = mahasiswa punya nilai (level scores), dan jumlah profil hasil preprocessing = yang
  punya data lengkap. Ini normal, bukan error.
- Nilai hanya dari subset mahasiswa yang **setuju membuka nilai** (bias seleksi).
- Akurasi klasifikasi ~0.54–0.62 → **realistis** untuk data perilaku; bukan angka "sihir".
  Justru bagus untuk presentasi karena jujur.