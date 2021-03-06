[Kembali ke readme](README.md)

# Testcase

## Deskripsi
Testcase ini digunakan sebagai parameter pengerjaan untuk setiap respon didapat dari command yang dikirim.

## Command

### USER
| Command                                                  | Response                            |
|----------------------------------------------------------|-------------------------------------|
| USER                                                     | `501 Missing required argument`     |
| USER [user_ada]                                          | `331 Please, specify the password.` |
| USER [user_tidak_ada]                                    | `331 Please, specify the password.` |

### PASS
| Command               | Response                |
|-----------------------|-------------------------|
| PASS                  | `530 Login incorrect.`  |
| PASS [password_salah] | `530 Login incorrect.`  |
| PASS [password_benar] | `230 Login successful.` |

### PWD
Relative bergantung pada default folder di server
| Command | Response                        |
|---------|---------------------------------|
| PWD     | `257 "/" is current directory.` |

### MKD
| Command                        | Response                                            |
|--------------------------------|-----------------------------------------------------|
| MKD                            | `501 Missing required argument`                     |
| MKD[ada_spasi]                 | `550 Invalid file name or path`                     |
| MKD  [directory_tidak_ada]     | `550 Couldn't open the file or directory`           |
| MKD [nama_directory_sudah_ada] | `550 Directory with same name already exists.`      |
| MKD [nama_directory_belum_ada] | `257 "/[nama_dir_belum_ada]" created successfully.` |

### RNFR & RNTO:
| Command                                               | Response                                                                                              |
|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| RNFR                                                  | `501 Missing required argument`                                                                       |
| RNFR [directory_tidak_ada]                            | `550 Couldn't open the file or directory`                                                             |
| RNFR [directory_ada]                                  | `350 Directory exists, ready for destination name.`                                                   |
| RNTO                                                  | `501 Missing required argument`                                                                       |
| RNTO [nama_directory]                                 | `503 Use RNFR first.`                                                                                 |
| RNFR RNTO [nama_directory]                            | ``` 501 Missing required argument <br> 503 Use RNFR first. ```                                             |
| RNFR [nama_directory_sama] RNTO [nama_directory_sama] | ``` 350 Directory exists, ready for destination name. 250 File or directory renamed successfully. ``` |
| RNFR [nama_directory] RNTO [nama_directory_udah_ada]  | ``` 350 Directory exists, ready for destination name. 550 Permission denied ```                       |

### RMD
| Command                                               | Response                                                                                              |
|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| RMD                                                   | `501 Missing required argument`                                                                       |
| RMD [directory_ada]                                   | `250 Directory deleted successfully.`                                                                 |
| RMD [directory_tidak_ada]                             | `550 Couldn't open the file or directory`                                                             |

### DELE
| Command                                               | Response                                                                                              |
|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| DELE                                                  | `501 Missing required argument`                                                                       |
| DELE [folder]                                         | `550 Couldn't open the file`                                                                          |
| DELE [file_tidak_ada]                                 | `550 Couldn't open the file or directory`                                                             |
| DELE [file_tanpa_extension]                           | `550 Couldn't open the file or directory`                                                             |
| DELE [file_dengan_extension]                          | `250 File deleted successfully.`                                                                      |

### CWD
| Command                                               | Response                                                                                              |
|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| CWD                                                   | `501 Missing required argument`                                                                       |
| CWD [extenstion_file]                                 | `550 Couldn't open the file or directory`                                                             |
| CWD [folder_tidak_ada]                                | `550 Couldn't open the file or directory`                                                             |
| CWD [folder_ada]                                      | `550 Couldn't open the file or directory`                                                             |

### HELP
| Command | Response |
|---|---|
| HELP | ```214 The following commands are recognized.     NOP  USER TYPE SYST SIZE RNTO RNFR RMD  REST QUIT     HELP XMKD MLST MKD  EPSV XCWD NOOP AUTH OPTS DELE     CWD  CDUP APPE STOR ALLO RETR PWD  FEAT CLNT MFMT     MODE XRMD PROT ADAT ABOR XPWD MDTM LIST MLSD PBSZ     NLST EPRT PASS STRU PASV STAT PORT     214 Help ok.``` |

### QUIT
| Command | Response       |
|---------|----------------|
| QUIT    | `200 Goodbye.` |

### Kasus lain
| Command                                                          | Response                                      |
|------------------------------------------------------------------|-----------------------------------------------|
| [command_salah]                                                  | `500 Wrong command.`                          |
| [menjalankan command jika belum authenticated selain syst, feat] | `530 Please log in with USER and PASS first.` |
| [menjalankan command USER kembali setelah authenticated]         | `503 Already logged in. QUIT first.`          |
| [menjalankan command PASS setelah setelah authenticated]         | `503 Already logged in.`                      |
