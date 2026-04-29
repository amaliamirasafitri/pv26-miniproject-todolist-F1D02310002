Judul : **Aplikasi To-Do List**

**Deskripsi**
Aplikasi To-Do List merupakan aplikasi manajemen tugas berbasis desktop 
yang dibuat menggunakan bahasa pemrograman Python dengan library PySide6. 
Aplikasi ini digunakan untuk membantu pengguna mencatat dan mengelola tugas sehari-hari agar lebih teratur. 

**Cara menjalankannya** 
1. Aktifkan Virtual Environment **venv\Scripts\activate**
2. Install PySide6 (jika belum) **pip install PySide6**
3. Jalankan Aplikasi **python main.py**
4. Tampilan yang Akan Muncul
**Login Window (GUI, bukan CMD)
Setelah login → masuk ke halaman To-Do List**

**Teknologi yang digunakan**
1. Python Bahasa pemrograman utama untuk membuat logika aplikasi, seperti, tambah tugas, edit & delete, login user
2. PySide6 Digunakan untuk membuat tampilan GUI (aplikasi desktop), seperti, form login, tombol, list tugas, dialog tambah/edit
3. SQLite Digunakan sebagai database untuk menyimpan data tugas (task) dan data user (login)
4. QSS (Qt Style Sheet) Digunakan untuk mengatur tampilan aplikasi, seperti, warna tombol, font, layout, border & tampilan UI
5. Konsep Separation of Concerns (SoC) Struktur project dipisah menjadi ui/ → tampilan (GUI), database/ → pengolahan database, style/ → styling (QSS), main.py → menjalankan aplikasi
