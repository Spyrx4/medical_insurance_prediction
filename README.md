# Prediksi Biaya Asuransi Kesehatan dengan Machine Learning

## 📌 Tentang Dataset

Dataset asuransi kesehatan berisi informasi tentang sejumlah faktor yang dapat memengaruhi biaya medis, termasuk usia, jenis kelamin, IMT, status merokok, jumlah anak, dan wilayah. Dataset ini dapat digunakan untuk melatih model pembelajaran mesin yang dapat memprediksi biaya medis untuk pelanggan baru.

Untuk memberikan wawasan mengenai faktor-faktor utama yang menyebabkan biaya asuransi lebih tinggi dan membantu perusahaan membuat keputusan yang lebih tepat mengenai penetapan harga dan penilaian risiko.

### Kolom Data:
- **age**: Usia penerima asuransi (dalam tahun)
- **sex**: Jenis kelamin (`male` / `female`)
- **bmi**: Indeks Massa Tubuh (Body Mass Index)
- **children**: Jumlah anak yang ditanggung dalam polis
- **smoker**: Status merokok (`yes` / `no`)
- **region**: Wilayah tempat tinggal penerima asuransi (`northeast`, `northwest`, `southeast`, `southwest`)
- **charges**: Biaya medis (target prediksi)

## ❓ Problem Statement:

Proyek ini bertujuan untuk menjawab pertanyaan berikut:

1. **Apa faktor terpenting yang memengaruhi biaya pengobatan?**  
   Melalui analisis eksploratif dan interpretasi model, kita dapat mengidentifikasi variabel mana yang paling berkontribusi terhadap tingginya biaya asuransi.

2. **Seberapa baik model pembelajaran mesin dapat memprediksi biaya medis?**  
   Kami mengevaluasi kinerja beberapa algoritma regresi untuk menentukan model terbaik dalam memprediksi biaya berdasarkan fitur yang tersedia.

3. **Bagaimana model pembelajaran mesin dapat digunakan untuk meningkatkan efisiensi dan profitabilitas perusahaan asuransi kesehatan?**  
   Dengan prediksi yang akurat, perusahaan dapat menyesuaikan premi secara lebih adil, mengelola risiko lebih baik, dan mengurangi kerugian akibat underpricing.

## ⚙️ Instalasi & Setup

```bash
pip install -r requirements.txt

