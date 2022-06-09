[Kembali ke readme](README.md)

# List Command

- [X] Autentikasi (USER dan PASS: 4.1.1)

```
localhost
5656
USER ariesta
PASS suga123
```

- [X] Mengubah direktori aktif (CWD: 4.1.1)

```
localhost
5656
USER ariesta
PASS suga123
CWD foto-anya
```

- [X] Mencetak direktori aktif (PWD: 4.1.3)
```
localhost
5656
USER ariesta
PASS suga123
PWD
```

- [X] Keluar aplikasi (QUIT: 4.1.1)

```
localhost
5656
USER ariesta
PASS suga123
QUIT
```

- [X] Unduh (RETR: 4.1.3)

```
localhost
5656
USER ariesta
PASS suga123
PASV
RETR fuyukaidesu.jpg
```

- [X] Unggah (STOR: 4.1.3)

```
localhost
5656
USER ariesta
PASS suga123
CWD coba
PASV
STOR luffy.jpg
```

- [X] Mengganti nama file (RNTO: 4.1.3)
```
localhost
5656
USER ariesta
PASS suga123
RNFR ty2.jpeg
RNTO ty.jpeg
```

- [X] Menghapus file (DELE: 4.1.3)
```
localhost
5656
USER ariesta
PASS suga123
DELE luffy.jpg
```

- [X] Menghapus direktori (RMD: 4.1.3)
```
localhost
5656
USER ariesta
PASS suga123
RMD [bebas]
```

- [X] Membuat direktori (MKD: 4.1.3)
```
localhost
5656
USER ariesta
PASS suga123
MKD [bebas]
```

- [X] Mendaftar file dan direktori (LIST: 4.1.3)
```
localhost
5656
USER ariesta
PASS suga123
PASV
LIST
```

- [X] HELP: 4.1.3
```
localhost
5656
USER ariesta
PASS suga123
HELP
```

- [X] Reply codes (200 [OK], 500 [OK], 202 [OK], 230 [OK], 530 [OK]: 4.2.1)
- [X] Menerapkan teknik multiclient dengan modul select DAN thread
