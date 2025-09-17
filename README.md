Tautan aplikasi yang sudah dideploy: https://ardyana-feby-newgameshop.pbp.cs.ui.ac.id/
1. Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
    Karena dalam membuat platform tentunya pasti ada interaksi berupa data yang ditukar antara server dan pengguna. Dengan adanya data delivery baik user maupun server tidak bingung untuk membaca atau memproses interaksi yang ada antara user dan pengguna. Contoh, user sudah klik, jika tidak ada data delivery di platform, di server bisa jadi datanya tidak tersampaikan, apalagi server hanya bisa memproses data dari user dengan format yang jelas.

2. Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?
    Menurut saya JSOn lebih baik daripada XML karena JSON bisa menampilkan visualisasi sehingga terlihat lebih simple dan mudah dibaca dengan mata. Selain itu JSON juga sudah kompetibel langsung dengan JavaScript. XML memnag bagus untuk dokumen yang teksnya banyak, tetapi formatnya panjang dan lebih berat untuk di-parse.

3. Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?
    is_valid() di sini untuk buat ngecek apakah data yang diisi user udah benar atau belum sesuai aturan (misalnya field wajib, tipe angka, datatype valid). Jadi sebelum data masuk database, kita cek dulu dulu supaya tidak error.

4. Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?
    CSRF token untuk mencegah adanya Cross-Site Request Forgery, yaitu pihak ketiga "titip" permintaan POST/PUT/DELETE ke situs kita melalui sesi pengguna tanpa sepengetahuan mereka. Kalau tidak menggunakan CSRF token, orang jahat bisa bikin form palsu di luar sana tapi tetap mengirim request ke web kita pakai akun kita tanpa sadar. Sehingga bisa menimbulkan bahaya, seperti data kehapus atau akun ketakeover.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)
    Langkah pertama saya buat model, model ini sebagai representasi“bentuk data” yang ingin disimpan ke database. Model inin yang nanti akan almemastikan bahwa data yang tersimpan memiliki format dan atribut yang sesuai, seperti nama, harga, deskripsi, dll. Selanjutnya membuat form di direktory main. Dengan form ini, user bisa memasukkan data lewat halaman web. Nah, form ini juga sekalian ngecek validasi supaya data yang masuk benar (misalnya harga angka, bukan huruf). Selanjutnya di views.py saya menambahkan beberapa fungsi sebagai penghubung model, form, dan template. Di sini saya membuat fungsi untuk menampilkan daftar item, menambahkan data baru, menampilkan detail, dsb. Setelah views selesai, setiap fungsi perlu dihubungkan dengan alamat URL tertentu. Routing ini memastikan bahwa setiap permintaan pengguna diarahkan ke fungsi yang sesuai. Selanjutnya supaya lebih menarik dan informatis tampilannya di halaman html (main.html), saya menambahkan tombol "Add" dan "Details untuk melihat detail produk yang ingin diklik. Setelah itu saya akses local host dengan /xml/ dan /json/ untuk mengecek di POstman, apakah datanya sudah keluar dengan format benar atau belum.

6. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
    So far, ga ada kendala atau masukkan sih karena kakak asdosnya juga informatif dan cepat tanggap, ga perlu tunggu respon lama langsung dibales. Jadi pas di luar kelas tutor, tutorialnya udah selesai dan bisa tenang pelajarin apa yang udah disampaiin di berkas tutor tadi.

Screenshoot Postman:
https://drive.google.com/drive/folders/19zmS5ZTEdGVkPybv1Brvbl_or4xl-NZX?usp=sharing