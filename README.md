# SmartMatch Laptop Recommendation System

SmartMatch adalah aplikasi rekomendasi laptop berbasis **Streamlit** yang menggabungkan **Fuzzy Logic** dan **Particle Swarm Optimization (PSO)** untuk membantu memilih laptop sesuai budget dan preferensi pengguna.

## Fitur

- Rekomendasi laptop berdasarkan budget, RAM, storage, berat, performa, dan baterai
- Visualisasi proses optimasi PSO
- Perbandingan beberapa laptop terpilih
- Dukungan mata uang **IDR**, **USD**, dan **EUR**

## Struktur Proyek

- `app.py` - antarmuka utama Streamlit
- `fuzzy.py` - logika fuzzy untuk menilai kecocokan laptop
- `pso.py` - optimasi PSO untuk mencari spesifikasi optimal
- `laptop_price - dataset.csv` - dataset laptop yang digunakan aplikasi
- `presentation_script_python.md` - materi/script presentasi

## Persyaratan

- Python 3.10 atau lebih baru
- Paket Python:
  - `streamlit`
  - `numpy`
  - `matplotlib`

## Instalasi

Jalankan perintah berikut di folder project:

```bash
python -m pip install streamlit numpy matplotlib
```

## Menjalankan Aplikasi

```bash
streamlit run app.py
```

Setelah itu, buka alamat yang ditampilkan di terminal, biasanya:

```text
http://localhost:8501
```

## Catatan

- Pastikan file `laptop_price - dataset.csv` berada di folder project yang sama dengan `app.py`.
- Jika dataset tidak terbaca, aplikasi akan menampilkan pesan error dan berhenti.

## GitHub

Repository: https://github.com/gusti06/Tubes-KK-SmartMatch-