# Membuat FTP Server dan Klien

## Anggota

1. 05111940000105 - I Kadek Agus Ariesta Putra
2. 05111940000161 - Timotius Wirawan

## Ketentuan
Mengimplementasikan RFC 959 (dituliskan dengan subbab) sebagai berikut

- [X] Membuat aplikasi FTP klien dan server
- [X] Autentikasi (USER dan PASS: 4.1.1)
- [X] Mengubah direktori aktif (CWD: 4.1.1)
- [X] Keluar aplikasi (QUIT: 4.1.1)
- [X] Unduh (RETR: 4.1.3)
- [X] Unggah (STOR: 4.1.3)
- [X] Mengganti nama file (RNTO: 4.1.3)
- [X] Menghapus file (DELE: 4.1.3) 
- [X] Menghapus direktori (RMD: 4.1.3)
- [X] Membuat direktori (MKD: 4.1.3)
- [X] Mencetak direktori aktif (PWD: 4.1.3)
- [X] Mendaftar file dan direktori (LIST: 4.1.3)
- [X] HELP: 4.1.3
- [X] Reply codes (200 [OK], 500 [OK], 202 [OK], 230 [OK], 530 [OK]: 4.2.1)
- [X] Menerapkan teknik multiclient dengan modul select DAN thread

## Testcase
Kami telah melakukan mencantumkan list response dari command yang dikirim menggunakan referensi pada Filezilla. List response bisa dilihat pada file [testcase](testcase.md)

## Command
Kami telah mencantumkan command yang dibutuhkan untuk mewakilkan setiap studi kasus yang ada. List command dilihat pada file [command](command.md)