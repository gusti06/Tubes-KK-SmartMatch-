# 🗣️ Skrip Video Presentasi Proyek SmartMatch (Versi Python)
## Proyek: SmartMatch - Sistem Rekomendasi Laptop Hybrid (Fuzzy Logic + PSO)
### Panduan & Naskah Presentasi Kelompok (5 Orang - Maksimal 15 Menit)

Naskah ini dirancang khusus untuk memenuhi standar **Video Presentasi** tugas besar:
1. **Penjelasan latar belakang & definisi masalah.**
2. **Penjelasan cara kerja metode penyelesaian (Fuzzy Logic & PSO).**
3. **Simulasi/Demo Aplikasi secara *real-time*.**

Setiap pembicara memiliki porsi waktu ±2.5 hingga 3 menit agar total durasi video aman di kisaran **12 - 14 menit** (maksimal 15 menit).

---

## 🎤 PEMBICARA 1: Latar Belakang, Definisi Masalah, & Arsitektur Hybrid
* **Tanggung Jawab**: Pembukaan video, latar belakang masalah, perumusan masalah komputasional, penjelasan arsitektur hibrida (Fuzzy + PSO), dan loading dataset.
* **Tampilan Visual (Visual Cue)**: Slide Presentasi (Judul, Latar Belakang Masalah, Diagram Arsitektur Sistem Hybrid) & Tampilan File [app.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/app.py) di editor kode bagian pemuatan dataset.
* **Estimasi Durasi**: 2.5 Menit

**[NASKAH DIALOG]**

"Halo semuanya. Kami dari Kelompok Proyek SmartMatch akan mempresentasikan hasil kerja kami dalam membangun **Sistem Rekomendasi Laptop Hybrid** menggunakan perpaduan **Logika Fuzzy** dan **Particle Swarm Optimization (PSO)** berbasis Python.

**Latar Belakang & Definisi Masalah:**
Memilih laptop di era sekarang bukanlah perkara mudah. Calon pembeli sering kali dihadapkan pada ratusan pilihan dengan kombinasi spesifikasi RAM, Prosesor, Kartu Grafis, Berat, Kapasitas Baterai, dan harga yang sangat bervariasi. 

Masalah utama yang kami identifikasi dibagi menjadi dua aspek kecerdasan komputasional:
1. **Ketidakpastian Preferensi Subjektif (Fuzzy):** Kriteria manusia sering kali bersifat tidak pasti atau linguistik. Kata-kata seperti *'budget sedang'*, *'laptop ringan'*, atau *'performa tinggi'* tidak memiliki batas numerik yang kaku. Masalah ketidakpastian ini diselesaikan menggunakan **Logika Fuzzy**.
2. **Pencarian Multi-Dimensi (PSO):** Mencari titik kombinasi spesifikasi ideal (misalnya keseimbangan optimal antara harga murah, bobot ringan, dan performa maksimal) di dalam ribuan kombinasi spesifikasi adalah masalah optimasi ruang pencarian yang sangat luas. Masalah optimasi pencarian ini diselesaikan menggunakan **Particle Swarm Optimization (PSO)**.

**Arsitektur Sistem Hybrid:**
Sistem kami bekerja secara **Hibrida**. Pertama, preferensi pengguna dimasukkan ke dalam sistem. Algoritma PSO akan berjalan di latar belakang sebagai agen pencari cerdas untuk menentukan titik koordinat spesifikasi virtual yang 'paling ideal' berdasarkan aturan Fuzzy. Setelah titik optimal virtual ($g_{best}$) ditemukan, sistem akan memetakan dan mengurutkan laptop-laptop nyata di dalam dataset berdasarkan jarak geometris terdekat menggunakan rumus jarak Euclidean terbobot.

Mari kita lihat implementasi awalnya pada kode program. Di file [app.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/app.py) baris 55, kami mendefinisikan fungsi `load_dataset` untuk membaca dataset laptop nyata secara dinamis dari file CSV **[laptop_price - dataset.csv](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/laptop_price%20-%20dataset.csv)** menggunakan library internal `csv.DictReader`. Data tersebut kemudian dipreproses secara langsung agar siap digunakan untuk evaluasi matematis.

Selanjutnya, Pembicara 2 akan menjelaskan detail bagaimana data diproses menggunakan Logika Fuzzy."

---

## 🎤 PEMBICARA 2: Cara Kerja Metode - Logika Fuzzy (Fuzzifikasi & Evaluasi Aturan)
* **Tanggung Jawab**: Penjelasan penentuan performa/baterai, fungsi keanggotaan segitiga & trapesium, evaluasi aturan kebutuhan pengguna (Rules), dan defuzzifikasi.
* **Tampilan Visual (Visual Cue)**: Kode editor membuka file [fuzzy.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/fuzzy.py), menyorot fungsi `trimf`, `trapmf`, `estimate_performance_score`, dan aturan logika di `evaluate_laptop_suitability`.
* **Estimasi Durasi**: 3 Menit

**[NASKAH DIALOG]**

"Terima kasih Pembicara 1. Sekarang saya akan menjelaskan mesin logika fuzzy yang menjadi landasan penilaian di file [fuzzy.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/fuzzy.py).

Sebelum data masuk ke fungsi fuzzy, kami menyintesis atribut teknis laptop menjadi dua skor bernilai $0$ hingga $100$, yaitu `perfScore` (skor performa) dan `batteryScore` (skor daya tahan baterai). Sebagai contoh, pada fungsi `estimate_performance_score` di baris 29, skor performa ditentukan dari gabungan linear:
$$\text{perfScore} = 0.3 \cdot \text{skor\_RAM} + 0.4 \cdot \text{skor\_CPU} + 0.3 \cdot \text{skor\_GPU}$$
Di mana skor CPU disesuaikan secara linear berdasarkan clock speed terhadap baseline 2.5 GHz.

**Fuzzifikasi & Fungsi Keanggotaan:**
Di baris 5 sampai 26, kami mengimplementasikan dua fungsi keanggotaan matematika:
1. `trimf(x, a, b, c)`: Fungsi segitiga untuk variabel bernilai menengah.
2. `trapmf(x, a, b, c, d)`: Fungsi trapesium untuk nilai ekstrim bawah (murah/ringan) atau atas (mahal/berat).

Fungsi-fungsi ini memetakan nilai tegas spesifikasi laptop ke derajat keanggotaan fuzzy dalam rentang $[0, 1]$. Sebagai contoh, variabel **Berat** (`weight`) didefinisikan menjadi tiga himpunan fuzzy di baris 153:
* `ringan`: `trapmf(weight, 0, 0, 1.2, 1.6)`
* `sedang`: `trimf(weight, 1.4, 2.0, 2.6)`
* `berat`: `trapmf(weight, 2.3, 3.0, 100, 100)`

**Rule Evaluation (Evaluasi Aturan):**
Di dalam fungsi `evaluate_laptop_suitability` (baris 174), preferensi pengguna dicocokkan dengan spesifikasi laptop. Salah satu contoh penting adalah pencocokan budget di baris 180. Jika harga laptop berada di bawah budget, tingkat kecocokannya bernilai `1.0`. Namun, jika melebihi budget, nilai kecocokan akan menurun secara linear hingga batas toleransi 30%:
$$\text{budget\_match} = \max\left(0.0, 1.0 - \frac{\text{persen\_kelebihan}}{0.3}\right)$$

Selanjutnya, aturan kebutuhan spesifik dievaluasi di baris 218. Kami menggunakan logika matematika fuzzy untuk menggabungkan variabel: operator **ATAU (OR)** diwakili oleh fungsi `max()`, dan operator **DAN (AND)** diwakili oleh fungsi `min()`.
Sebagai contoh, perhatikan aturan untuk kebutuhan **Programming** di baris 229:
```python
rule_val = min(
    max(m['performance']['sedang'], m['performance']['tinggi']),
    ram_ok,
    max(m['price']['sedang'], m['price']['mahal'])
)
```
Aturan ini menyatakan bahwa laptop cocok untuk programming jika performanya sedang atau tinggi, kapasitas RAM mencukupi, DAN harganya berada di kategori sedang atau mahal (menandakan kualitas komponen pendukung).

**Defuzzifikasi:**
Kecocokan akhir dihitung menggunakan metode rata-rata terbobot dari seluruh kecocokan parameter (Budget 25%, RAM 15%, Storage 10%, Berat 15%, Performa 15%, Baterai 10%, dan Kebutuhan 10%). Hasil penjumlahan terbobot ini dikalikan 100 untuk menghasilkan skor persentase bulat $0\% - 100\%$.

Selanjutnya, Pembicara 3 akan memaparkan bagaimana PSO mencari koordinat spesifikasi laptop impian tersebut."

---

## 🎤 PEMBICARA 3: Cara Kerja Metode - Particle Swarm Optimization (PSO)
* **Tanggung Jawab**: Penjelasan peran PSO, inisialisasi partikel, pembatasan ruang pencarian (4 dimensi), pembaruan kecepatan dan posisi, efek bouncing (pemantulan batas), dan fitness evaluation.
* **Tampilan Visual (Visual Cue)**: Kode editor menyorot file [pso.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/pso.py), fokus pada inisialisasi konstanta hiperparameter PSO (`w`, `c1`, `c2`), rumus update posisi/kecepatan, dan logika *bouncing* di dalam kelas `Particle`.
* **Estimasi Durasi**: 3 Menit

**[NASKAH DIALOG]**

"Terima kasih Pembicara 2. Sekarang kita masuk ke bagian inti mesin pencari optimasi kawanan partikel kita di file [pso.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/pso.py).

Kenapa kita membutuhkan PSO? Jika kita hanya melakukan pencarian linier satu per satu pada database, kita tidak akan tahu kombinasi spesifikasi ideal teoritis yang paling seimbang untuk preferensi pengguna. Di sinilah PSO bertindak sebagai agen optimasi yang mencari koordinat optimal dalam **ruang pencarian 4 dimensi**:
1. Dimensi 0: Harga (150 hingga 4000 Euro)
2. Dimensi 1: RAM (2 hingga 32 GB)
3. Dimensi 2: Berat (0.6 hingga 4.5 kg)
4. Dimensi 3: Performa (10 hingga 100)

**Pembaruan Kecepatan & Posisi Partikel:**
Di dalam kelas `PSOManager` (baris 48), kami menginisialisasi 40 partikel. Masing-masing partikel dibekali dengan koordinat posisi, vektor kecepatan acak, dan memori posisi terbaik pribadinya sendiri ($p_{best}$).
Hiperparameter PSO yang kami gunakan mengikuti standar optimasi global (baris 67):
* **Inertia Weight ($w$) = 0.729** (menjaga momentum kecepatan partikel agar tidak langsung berhenti).
* **Cognitive Coefficient ($c_1$) = 1.494** (gaya tarik partikel ke arah pengalaman terbaik pribadinya sendiri).
* **Social Coefficient ($c_2$) = 1.494** (gaya tarik partikel ke arah posisi terbaik yang pernah ditemukan oleh seluruh kawanan, yaitu $g_{best}$).

Pada fungsi `step` di baris 131, kecepatan tiap partikel diubah menggunakan rumus pembaruan kecepatan standar:
$$v_i(t+1) = w \cdot v_i(t) + c_1 \cdot r_1 \cdot (p_{best, i} - x_i(t)) + c_2 \cdot r_2 \cdot (g_{best} - x_i(t))$$
Di mana $r_1$ dan $r_2$ adalah nilai acak antara $0.0$ dan $1.0$.

**Boundary Clamping & Bouncing:**
Satu tantangan dalam PSO adalah partikel yang terbang keluar dari batas ruang pencarian logis (misalnya harga minus atau RAM bernilai ribuan). Kami menerapkan logika **Boundary Clamping & Bouncing** di baris 38 pada file [pso.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/pso.py):
```python
if self.position[i] < self.bounds[i]['min']:
    self.position[i] = self.bounds[i]['min']
    self.velocity[i] = -self.velocity[i] * 0.5
```
Jika partikel menabrak batas minimum atau maksimum, posisinya akan dikunci di batas tersebut dan kecepatannya akan dibalikkan arahnya (dipantulkan) serta diredam sebesar 50% agar partikel kembali berfokus mengeksplorasi area dalam batas ruang pencarian.

**Fungsi Fitness:**
Kualitas posisi kawanan partikel dievaluasi menggunakan metode `evaluate_spec_fitness` (baris 78). Fungsi ini mengambil koordinat 4D dari partikel, menyusun data laptop virtual tiruan, lalu mengevaluasi nilai kecocokan koordinat tersebut menggunakan fungsi logika fuzzy `evaluate_laptop_suitability` dari Pembicara 2. Dengan demikian, partikel dituntun untuk bergerak menuju koordinat spesifikasi laptop virtual yang paling memuaskan kebutuhan pengguna.

Selanjutnya, Pembicara 4 akan memaparkan bagaimana pencocokan hibrida dilakukan terhadap laptop nyata di dataset serta visualisasi grafiknya."

---

## 🎤 PEMBICARA 4: Cara Kerja Metode - Integrasi Sistem Hybrid & Visualizer Plot
* **Tanggung Jawab**: Penjelasan pencocokan hibrida (Euclidean terbobot & skor gabungan), integrasi visualisasi real-time Matplotlib (Sumbu X & Y, legenda non-overlapping, background constellation), dan loop animasi Streamlit.
* **File Referensi**: [app.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/app.py) (baris 86-143 dan 294-392)
* **Tampilan Visual (Visual Cue)**: Kode editor menyorot file [app.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/app.py) bagian fungsi `calculate_distance_to_optimal`, `get_recommendations`, dan pembuatan objek plot matplotlib `render_plot`.
* **Estimasi Durasi**: 2.5 Menit

**[NASKAH DIALOG]**

"Terima kasih Pembicara 3. Sekarang kita akan melihat bagaimana titik optimal virtual ($g_{best}$) hasil perhitungan PSO digabungkan dengan laptop fisik dari dataset.

**Pencocokan Hibrida (Hybrid Matching):**
Koordinat optimal virtual hasil PSO ($g_{best}$) belum tentu ada secara persis di dunia nyata. Oleh karena itu, di file [app.py](file:///d:/kuliah/semester%206/Kecerdasan%20Komputasional/tubes%202%20real/app.py) baris 86, kami mengimplementasikan pencocokan hibrida melalui fungsi `calculate_distance_to_optimal`. 
Kami mengukur seberapa dekat setiap laptop riil di dataset dengan koordinat spesifikasi optimal teoritis tersebut menggunakan **Jarak Euclidean Terbobot (Weighted Euclidean Distance)**:
$$\text{dist} = \sqrt{0.35 \cdot (\Delta \text{Harga})^2 + 0.25 \cdot (\Delta \text{RAM})^2 + 0.15 \cdot (\Delta \text{Berat})^2 + 0.25 \cdot (\Delta \text{Performa})^2}$$
Semua selisih dimensi telah dinormalisasi ke rentang $0$ hingga $1$ agar tidak timpang secara nilai. Jarak ini dikonversi menjadi persentase kedekatan geometris:
$$\text{proximity\_score} = \max(0.0, (1.0 - \text{dist}) \cdot 100.0)$$

Di baris 116, skor rekomendasi final diperoleh dari gabungan:
$$\text{Skor Final} = 0.7 \cdot \text{Skor Fuzzy} + 0.3 \cdot \text{Skor Proximity Geometric}$$
Dengan metode hibrida ini, laptop yang direkomendasikan tidak hanya cocok secara aturan logika fuzzy, tetapi juga memiliki spesifikasi yang sedekat mungkin secara fisik ke target optimal virtual yang dicari oleh PSO.

**Visualisasi Grafis Matplotlib:**
Untuk memvisualisasikan pergerakan partikel secara real-time, kami merancang fungsi `render_plot` di baris 310 menggunakan **Matplotlib** dengan tema gelap (`plt.style.use('dark_background')`).
* Sumbu X merepresentasikan **Harga** (Euro) dan Sumbu Y merepresentasikan **Performa** (skala 0-100).
* Agar visualisasi terlihat mewah, kami menggambar seluruh laptop di dataset sebagai sebaran bintang galaksi yang sangat redup di latar belakang menggunakan parameter `alpha=0.04`.
* Partikel aktif diplot dengan warna biru neon, sedangkan target global best ($g_{best}$) ditandai dengan simbol target besar berwarna ungu yang berpendar.
* Informasi legenda diletakkan di bagian bawah luar sumbu (`bbox_to_anchor=(0.5, -0.25)`) dengan format 3 kolom agar rapi dan tidak menutupi visualisasi pergerakan partikel.
* Grid digambar dengan garis titik-titik tipis (`linestyle=':'`) menggunakan tuple warna transparan untuk menjaga kerapian visual.

Di baris 378, loop iterasi PSO dijalankan secara visual di Streamlit. Melalui elemen placeholder `plot_placeholder.pyplot()`, visualisasi diperbarui setiap 2 iterasi dan diberi jeda frame `time.sleep(0.02)` untuk menampilkan animasi kawanan partikel yang mengeksplorasi data lalu secara konvergen berkumpul ke target $g_{best}$.

Selanjutnya, Pembicara 5 akan mendemonstrasikan aplikasi ini secara langsung."

---

## 🎤 PEMBICARA 5: Demo Aplikasi Real-Time & Penutupan
* **Tanggung Jawab**: Menunjukkan antarmuka aplikasi di browser secara live, demonstrasi interaksi widget, eksekusi tombol cari, penayangan animasi partikel PSO, ulasan kartu rekomendasi laptop, demo fitur komparasi spesifikasi, dan penutup presentasi.
* **Tampilan Visual (Visual Cue)**: Perekaman layar browser menampilkan aplikasi Streamlit (`http://localhost:8501`). Lakukan demo interaksi mengubah input budget/RAM, menekan tombol cari, melihat pergerakan visualisasi plot partikel, scroll hasil kartu laptop, mencentang checkbox perbandingan, dan menampilkan tabel komparasi.
* **Estimasi Durasi**: 3 Menit

**[NASKAH DIALOG]**

"Terima kasih Pembicara 4. Sekarang, mari kita lihat demonstrasi langsung dari aplikasi **SmartMatch** yang berjalan di platform Streamlit ini.

Seperti yang Anda lihat pada layar, antarmuka pengguna dirancang dengan tema gelap yang premium. 
Di panel sebelah kiri (sidebar), pengguna dapat memasukkan preferensi mereka:
1. Kita pilih mata uang, misalnya **IDR (Rupiah)**.
2. Kita atur budget maksimal, misalnya **Rp 20.000.000**. Secara dinamis, sistem langsung menampilkan nilai konversinya dalam Euro dan USD di bawahnya.
3. Kita tentukan kriteria minimal, seperti RAM minimum **8 GB**, Portabilitas **Bebas**, dan Prioritas Performa Utama **Performa Tinggi**.
4. Kita centang kebutuhan penggunaan kita, misalnya **Kuliah / Kerja** dan **Programming**.

Sekarang, saya akan menekan tombol **'Cari Laptop Terbaik (PSO)'**.

Perhatikan pada panel visualisasi di sebelah kiri. Kumpulan partikel biru neon mulai tersebar secara acak di area diagram pencarian. Dalam hitungan detik, partikel-partikel tersebut bergerak secara dinamis, mendekat, dan akhirnya berkumpul atau konvergen ke satu titik target berwarna ungu, yaitu spesifikasi optimal virtual yang paling menyeimbangkan preferensi kita. Di bawah grafik, tertera statistik iterasi yang menunjukkan konvergensi selesai di iterasi ke-80 dengan kecocokan terbaik.

Mari beralih ke panel sebelah kanan. Hasil rekomendasi laptop nyata yang paling mendekati spesifikasi ideal langsung ditampilkan secara menurun berdasarkan persentase kecocokan.
Kartu laptop ini dirancang menggunakan CSS Glassmorphism yang elegan. Setiap kartu menunjukkan nama laptop, spesifikasi teknis lengkap, badge kecocokan (misalnya **94% Match**), harga dalam Rupiah, dan label rekomendasi berwarna hijau.

Salah satu fitur unggulan aplikasi kami adalah **Perbandingan Spesifikasi**. Di bawah setiap kartu laptop, terdapat checkbox perbandingan. Saya akan mencentang dua laptop teratas ini.
Secara instan, sistem akan membuat bagian baru di bawah bernama **'Perbandingan Laptop Terpilih'**. Di sini, spesifikasi utama kedua laptop disandingkan secara detail dalam tabel horizontal yang terstruktur, mulai dari harga, RAM, GPU, berat, hingga skor performa dan baterai hasil perhitungan Fuzzy Logic. Ini sangat membantu pengguna dalam membuat keputusan akhir.

Sebagai kesimpulan, transisi sistem rekomendasi SmartMatch ke versi Python Streamlit ini berhasil meningkatkan efisiensi pembacaan data langsung dari file CSV, memberikan visualisasi matematis PSO yang sangat lancar menggunakan Matplotlib, serta menyajikan antarmuka modern yang responsif bagi pengguna akhir.

Sekian presentasi dan demonstrasi dari kelompok kami. Terima kasih atas perhatian Bapak/Ibu Dosen dan rekan-rekan semua. Kami membuka sesi tanya jawab jika ada hal yang ingin didiskusikan lebih lanjut."
