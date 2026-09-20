Nama : Fiqhi Deski Ismail

NPM : 2506534245

Kelas : PBP B

# My Portofolio

Fullstack development of my own portofolio.

Built with django fullstack

## Prerequisites

- Python with `pip` and `venv`
- Node.js with npm (for Tailwind CSS and Prettier)
- Git

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/iD3sk/portofolio.git myportofolio
cd myportofolio
```

Run the following commands from this project folder.

### 2. Create and activate a virtual environment

**Create it (run once):**

```bash
python -m venv env
```

Windows (PowerShell):

```powershell
.\env\Scripts\Activate
```

macOS / Linux (use `python3` instead of `python` to create the environment if needed):

```bash
source env/bin/activate
```

After activation, `python` and `pip` use the project's virtual environment.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
npm ci
```

On Windows PowerShell, use `npm.cmd` instead of `npm` if script execution is blocked.

### 4. Prepare the database and CSS

```bash
python manage.py migrate
npm run build:css
```

The current local configuration uses SQLite and does not require a `.env` file or a separate database server. Migrations create the tables used by Django's built-in applications.

### 5. Start the development server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. Stop the server with `Ctrl+C`.

### 6. Watch CSS changes while developing

In a second terminal, open the same project folder and run:

```bash
npm run dev:css
```

Keep this command running while editing templates or `static/css/app.css`. Tailwind rebuilds `static/css/tailwind.css` automatically; refresh the browser to see changes. Do not edit the generated CSS directly.

<br>
<br>
<br>
<br>

# Tugas 1

Pada minggu ini aku menambahkan section experience dalam beberapa card

> Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

1. Ya, aku pake elemen semantik seperti section, main, atau article. elemen-elemen ini membantu agar memisahkan blok kode html yang memiliki makna tertentu, seperti section adalah satu blok section seperti landing page atau experience

<br>

> Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

2. Tantangannya menurutku adalah code readibility. untuk membuat layout responsif ini, aku pake cara mobil first-then desktop. perbedaan layout nya fokus ke user-experience. contoh pada tiap card experience, tahun dan content nya dibuat horizontal layout pada desktop, tetapi tidak cocok digunakan pada mobiile karena kekurangan space, makanya di mobile dibuat vertical.

<br>

> Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

3. keterbatasan web statis saat ini adalah aku harus hard code semua data-data experience yang aku miliki. Jika, experience ini terus bertambah aku harus hardcode lagi secara manual. fitur dinamis yang mungkin bisa ditambahkan adalah mengutilisasi database(?), sehingga data pada html yang akan dirender hanya perlu fetch dari database yang ada

## AI Disclosure

### Overview

Aku menggunakan AI-agentic jenis codex dengan model GPT-5.6 Sol. Aku menggunakan bantuan AI dalam hal:

1. Menjelaskan konsep dasar mengenai HTML, CSS, dan framework django secara general
2. Membantu menyusun design token dan migrasi dari vanilla css ke tailwind css
3. Saya juga meminta guide untuk layout responsive untuk mobile first, karena original templatenya menggunakan desktop first
4. Membantu konfigurasi dan penggunaan Prettier untuk formatting kode.
5. Memberikan penjelasan metode branching yang benar

### Strategi Prompting

Aku membagi permintaan bantuan AI berdasarkan kebutuhan yang spesifik, seperti penjelasan konsep, penyusunan design token, dan panduan migrasi CSS ke Tailwind. Untuk design token, fokus permintaanku adalah penyusunan nilai dasar styling yang dapat digunakan kembali agar tampilan website lebih konsisten.

### Keterbatasan AI

Dalam penyusunan design token, AI membantu menyediakan dasar styling, tetapi hasilnya belum sesuai dengan kebutuhan website portofolioku. Nilai warna, tipografi, dan jarak bisa terlihat masuk akal secara terpisah, tetapi belum menghasilkan tampilan yang nyaman dibaca ketika diterapkan bersama pada halaman. 

Karena itu, hasil AI perlu dievaluasi dalam konteks penggunaannya. Warna perlu diperiksa terhadap latar tempat teks ditampilkan, sedangkan ukuran teks dan jarak perlu dinilai berdasarkan konten halaman. Mengubah satu token juga dapat memengaruhi banyak elemen sekaligus, sehingga perbaikannya perlu mempertimbangkan seluruh bagian yang menggunakan token tersebut. AI membantu menyusun fondasi desain, tetapi hasilnya tetap memerlukan pemeriksaan dan keputusan manual.

### Perbaikan Manual

Aku menyesuaikan design token yang dihasilkan AI secara manual dengan mengacu pada design token dari website lain yang pernah aku kerjakan. Proses ini merupakan adaptasi design token: aku menggunakan proyek sebelumnya sebagai referensi untuk memperbaiki hasil AI sesuai kebutuhan desain website ini. Dengan demikian, hasil AI menjadi titik awal yang aku revisi berdasarkan referensi dan pengalaman pengerjaan sebelumnya.


Referensi log chat:

```bash
https://chatgpt.com/s/cx_6a9ed348faf48191bc47928a8c00a088
```


<br>
<br>
<br>
<br>


# Tugas 2

Pada minggu ini, aku membuat halaman `/about/` yang menampilkan profil singkat, education, dan achievement. Aku juga merapikan struktur template menggunakan `base.html` sebagai template utama. Navbar dan footer dipisahkan menjadi komponen agar dapat digunakan kembali pada halaman lain tanpa menulis ulang kode yang sama.

> Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.

<br>

1. Ketika pengguna membuka `/about/`, Django menerima request dan memeriksanya melalui `urls.py` proyek. File tersebut meneruskan routing ke `main/urls.py`, yang mencocokkan path `about/` dengan view `show_about`. View kemudian mengambil data pendidikan dan pencapaian dari model `Educations` dan `Achievements`. Data tersebut dimasukkan ke dalam context dan dikirim ke `about.html`. Template memproses context dengan Django Template Language, lalu Django mengembalikan hasil HTML kepada browser.

<br>

> Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

2. Data sebaiknya disimpan dalam model karena model menjadi struktur utama untuk menyimpan dan mengambil data dari database. Dengan begitu, perubahan pada pendidikan atau pencapaian dapat dilakukan melalui database tanpa mengubah struktur HTML. Template hanya bertugas menampilkan data yang diterima dari view. Pemisahan ini membuat kode lebih mudah dipelihara, mengurangi pengulangan, dan mempermudah penambahan fitur seperti formulir atau halaman admin pada pengembangan berikutnya.

<br>

> Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

3. `makemigrations` membuat file migration berdasarkan perubahan yang terdeteksi pada model, sedangkan `migrate` menerapkan isi file migration tersebut ke database. Contohnya, ketika aku menambahkan model `Educations` dan `Achievements`, aku menjalankan `python manage.py makemigrations` untuk mencatat struktur tabel yang baru. Setelah itu, aku menjalankan `python manage.py migrate` agar tabel tersebut benar-benar dibuat di database.

## AI Disclosure

### Overview

Aku menggunakan AI agent Codex untuk membantu pengerjaan Tugas 2 dalam hal:

1. Menjelaskan penggunaan template inheritance melalui `base.html` serta komponen navbar dan footer.
2. Membantu menyusun seeding data pendidikan dan pencapaian dari file Python.
3. Menjelaskan hubungan antara model, migration, database, view, context, dan template pada Django.
4. Membantu membuat tampilan rank gold, silver, dan bronze serta mengatur layout logo pencapaian.
5. Membantu menelusuri error `no such table` pada model Experience.

### Strategi Prompting

Aku memberikan prompt secara bertahap sesuai bagian yang sedang dikerjakan. Aku memulai dari pertanyaan konsep, lalu memberikan konteks file aktif dan meminta AI memeriksa implementasi yang sudah ada. Saat menemukan error, aku menyampaikan pesan error dan perubahan terakhir agar AI dapat menelusuri penyebabnya dari model, migration, database, dan proses server.

### Keterbatasan AI

Jawaban AI tidak selalu langsung sesuai dengan kondisi proyek. Contohnya, perubahan nama model dari `Experience` menjadi `Experiences` membuat Django mencari tabel dengan nama berbeda, walaupun tabel dan data lama masih ada. Beberapa saran layout juga tetap perlu diperiksa langsung karena hasil akhirnya bergantung pada ukuran layar dan susunan konten.

### Perbaikan Manual

Aku menentukan isi data, urutan tampil, dan keputusan visual pada halaman About. Aku juga memeriksa kembali nama model dan referensinya di view, menjalankan migration, serta menguji halaman melalui browser. Saran dari AI digunakan sebagai panduan, kemudian disesuaikan dengan struktur dan kebutuhan proyekku.

Referensi log chat:

```bash
https://chatgpt.com/s/cx_6aa53a0b98608191855503fb5b0d798e
```


<br>
<br>
<br>
<br>


### Tugas 3

Pada minggu ini, aku membuat fitur create, update, dan delete untuk data achievement menggunakan `ModelForm`. Data achievement juga dapat serialisasi dalam format JSON, kemudian di-deserialisasi sebelum ditampilkan kembali pada halaman About.

> Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!

<br>

1. `ModelForm` digunakan karena Django dapat membentuk field form, menjalankan validasi, dan menyimpan data berdasarkan definisi model. Dengan demikian, aku tidak perlu menulis ulang struktur dan aturan setiap field secara manual serta dapat menjaga form tetap konsisten dengan model. `{% csrf_token %}` diperlukan pada form yang mengirim request `POST` untuk memastikan request berasal dari halaman yang sah. Django akan memvalidasi token tersebut agar pihak lain tidak dapat mengirim request atas nama pengguna melalui serangan Cross-Site Request Forgery (CSRF).

<br>

> Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

2. JSON lebih disukai karena sintaksnya lebih ringkas sehingga ukuran data dan proses parsing umumnya lebih sederhana. Struktur object dan array pada JSON juga sesuai dengan struktur data JavaScript, sehingga dapat langsung diproses menggunakan fitur bawaan browser. XML lebih panjang karena menggunakan tag pembuka dan penutup serta biasanya memerlukan parser dan penanganan struktur yang lebih kompleks.

<br>

> Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

3. Saat halaman About dibuka, view mengambil data `Achievements` dari database melalui QuerySet. Fungsi `get_achievement_json` mengubah QuerySet tersebut menjadi JSON menggunakan `serializers.serialize`, lalu mengembalikannya sebagai `HttpResponse` dengan content type `application/json`. Pada `show_about`, respons JSON tersebut di-deserialisasi kembali menjadi object Python, dimasukkan ke dalam context, lalu ditampilkan oleh template. Serialization diperlukan karena instance model dan QuerySet merupakan object Python yang tidak dapat langsung dikirim melalui HTTP sebagai JSON. Proses tersebut mengubah field model menjadi representasi teks yang dapat dipertukarkan antara server dan client.

## AI Disclosure

### Overview

Aku menggunakan AI agent Codex untuk membantu pengerjaan Tutorial dan Tugas 3 dalam hal:

1. Menjelaskan perbedaan antara contoh Project pada tutorial dan implementasi yang perlu disesuaikan dengan bagian portofolioku.
2. Menjelaskan alur `ModelForm`, validasi form, penyimpanan data, serta hubungan antara field model dan input HTML.
3. Membantu menyesuaikan form Experience dan Achievement dengan struktur model yang digunakan.
4. Membantu menelusuri class Tailwind pada widget form yang belum masuk ke hasil build CSS.
5. Membantu menyusun jawaban reflektif Tugas 3 berdasarkan implementasi yang telah dibuat.

### Strategi Prompting

Aku memberikan konteks file dan bagian yang sedang dikerjakan, kemudian mengajukan pertanyaan secara bertahap mengenai konsep dan alur framework. Saat terdapat masalah pada form atau styling, aku menunjukkan implementasi yang sudah ada dan meminta AI menjelaskan penyebabnya sebelum menyesuaikan solusi dengan model serta design token proyekku.

### Keterbatasan AI

AI terkadang memberikan solusi yang terlalu umum atau mengasumsikan struktur proyek yang berbeda. Beberapa saran juga menggunakan pendekatan yang belum dibahas dalam tutorial. Karena AI tidak selalu memahami seluruh kondisi proyek dan hasil tampilan di browser, kode yang diberikan tetap perlu diperiksa, diuji, dan disesuaikan secara manual.

### Perbaikan Manual

Aku memeriksa setiap saran AI terhadap materi tutorial dan struktur proyek yang sebenarnya sebelum menerapkannya. Aku menyesuaikan nama model, field, URL, view, dan template dengan bagian Experience dan Achievement milikku, lalu menguji alur create, update, delete, serta data delivery. Aku juga memeriksa hasil tampilan secara langsung dan menyesuaikan styling form serta tombol agar tetap konsisten dengan desain portofolio.
