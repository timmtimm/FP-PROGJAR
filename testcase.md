[Kembali ke readme](readme.md)

# Testcase

## Deskripsi
Testcase ini digunakan sebagai parameter pengerjaan untuk setiap respon didapat dari command yang dikirim.

## Command

### USER
- "USER" => `501 Missing required argument`
- "USER [user_ada]" => `331 Please, specify the password.`
- "USER [user_tidak_ada]" => `331 Please, specify the password.`

### PASS
- "PASS" => `530 Login incorrect.`
- "PASS [password_salah] => `530 Login incorrect.`
- "PASS [password_benar]" => `230 Login successful.`

### PWD
Relative bergantung pada default folder di server
- "PWD" => `257 "/" is current directory.`

### MKD
- "MKD" => `501 Missing required argument`
- "MKD  " => `550 Invalid file name or path`
- "MKD  [directory_tidak_ada]" => `550 Couldn't open the file or directory`
- "MKD [nama_directory_sudah_ada]" => `550 Directory with same name already exists.`
- "MKD [nama_directory_belum_ada]" => `257 "/[nama_dir_belum_ada]" created successfully.`

### RNFR & RNTO:
- "RNFR" => `501 Missing required argument`
- "RNFR [directory_tidak_ada]" => `550 Couldn't open the file or directory`
- "RNFR [directory_ada]" => `350 Directory exists, ready for destination name.`
- "RNTO" => `501 Missing required argument`
- "RNTO [nama_directory]" => `503 Use RNFR first.`

- "RNFR
   RNTO [nama_directory]" =>
        ```501 Missing required argument
        503 Use RNFR first.```

- "RNFR [nama_directory_sama]
   RNTO [nama_directory_sama]" =>
        ```350 Directory exists, ready for destination name.
        250 File or directory renamed successfully.```

- "RNFR [nama_directory]
   RNTO [nama_directory_udah_ada]" =>
        ```350 Directory exists, ready for destination name.
        550 Permission denied```

### RMD
- "RMD [directory_ada]" => `250 Directory deleted successfully.`
- "RMD [directory_tidak_ada]" => `550 Couldn't open the file or directory`

### DELE
- "DELE" => `501 Missing required argument`
- "DELE [folder]" => `550 Couldn't open the file`
- "DELE [file_tidak_ada]" => `550 Couldn't open the file or directory`
- "DELE [file_tanpa_ext]" => `550 Couldn't open the file or directory`
- "DELE [file_dengan_ext]" => `250 File deleted successfully.`

### CWD
- "CWD" => 501 Missing required argument
- "CWD [extenstion_file]" => `550 Couldn't open the file or directory`
- "CWD [folder_tidak_ada]" => `550 Couldn't open the file or directory`
- "CWD [folder_ada]" => `250 CWD command successful`

### HELP
- "HELP" =>
    214 The following commands are recognized.
    NOP  USER TYPE SYST SIZE RNTO RNFR RMD  REST QUIT
    HELP XMKD MLST MKD  EPSV XCWD NOOP AUTH OPTS DELE
    CWD  CDUP APPE STOR ALLO RETR PWD  FEAT CLNT MFMT
    MODE XRMD PROT ADAT ABOR XPWD MDTM LIST MLSD PBSZ
    NLST EPRT PASS STRU PASV STAT PORT
    214 Help ok.

### QUIT
- "QUIT" => 200 Goodbye.

### Kasus lain

#### Command salah
- "[command_salah]" => `500 Wrong command.`

#### Kasus lain
- "menjalankan command jika belum authenticated selain syst, feat" => `530 Please log in with USER and PASS first.`
- "menjalankan command USER kembali setelah authenticated" => `503 Already logged in. QUIT first.`
- "menjalankan command PASS setelah setelah authenticated" => `503 Already logged in.`