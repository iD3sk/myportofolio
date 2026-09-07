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

### AI Disclosure

Aku menggunakan AI-agentic jenis codex dengan model GPT-5.6 Sol. Aku menggunakan bantuan AI dalam hal:

1. Menjelaskan konsep dasar mengenai HTML, CSS, dan framework django secara general
2. Membantu menyusun design token dan migrasi dari vanilla css ke tailwind css
3. Saya juga meminta guide untuk layout responsive untuk mobile first, karena original templatenya menggunakan desktop first
4. Membantu konfigurasi dan penggunaan Prettier untuk formatting kode.
5. Memberikan penjelasan metode branching yang benar

Referensi log chat:

```bash
https://chatgpt.com/s/cx_6a9ed348faf48191bc47928a8c00a088
```
