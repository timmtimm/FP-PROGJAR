from http import client
from pickle import FALSE
import socket
import logging
import os
from os.path import exists
from pathlib import Path
from datetime import datetime
import time
import platform
from _thread import *
from urllib import response
from random import *
import subprocess
import shutil

BUFFER_SIZE=1024
# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6999

SERVER_DATA = {
    "USER" : "ariesta",
    "PASS" : "heart123"
}

CLIENT_DATA = {
    "USER" : None,
    "PASS" : None,
    "AUTHENTICATED" : False,
    "ENCODING": "ASCII",
    "REAL_WD" : "/mnt/e/FTP",
    "WD" : "/", # Working Directory
    "DATA_SOCK": {
        "H1": 127,
        "H2": 0,
        "H3": 0,
        "H4": 1,
        "P1": None,
        "P2": None,
    },
    "DATA_SOCKET" : None,
    "DATA_SOCKET_CONN": None,
    "PASV": None
}

LIST_COMMAND = [
    "USER", "SYST", "TYPE", "RNTO", "RNFR", "RMD",
    "QUIT", "HELP", "MKD", "DELE", "CWD", "CDUP",
    "STOR",  "RETR", "PWD", "FEAT", "LIST", "PASV"
]

def is_address_exist(host, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result_of_check = a_socket.connect_ex((host, port))
    a_socket.close()

    if result_of_check == 0:
        return True
    else:
        return False

ThreadCount = 0

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('[!] Listening on port %s ...' % SERVER_PORT)

def reply_cmd(conn, msg):
    print("REPLYING", msg)
    conn.sendall(msg.encode())

def send_datasock(data_sock, response):
    data_sock.sendall(response.encode())

def threaded_socket(client_connection):
    # Send Wellcome Message
    client_connection.sendall("220 Welcome to FTP Server Simulator 1.0\r\n".encode())

    # Get the client request
    while True:
        request=client_connection.recv(BUFFER_SIZE)
        print(request)
        request=request.decode()

        if len(request) == 0:
            break

        request = request.rstrip()
        cmd = request.split(" ")
        print("CMD", cmd[0])

        if "USER" == cmd[0]: # This command need an argument
            if cmd[0] + " " in request == False:
                response = "501 Missing required argument\r\n"
                reply_cmd(client_connection, response)
                continue

            if CLIENT_DATA["AUTHENTICATED"] == True:
                response = "503 Already logged in. QUIT first.\r\n"
                reply_cmd(client_connection, response)
                continue

            response = "331 Please, specify the password.\r\n"
            reply_cmd(client_connection, response)
            CLIENT_DATA["USER"] = request.split(cmd[0] + " ")[1]

        elif "PASS" == cmd[0]: # This command need an argument

            if CLIENT_DATA["AUTHENTICATED"] == True:
                response = "503 Already logged in.\r\n"
                reply_cmd(client_connection, response)
                continue

            passwd = ""
            if cmd[0] + " " in request:
                passwd = request.split(cmd[0] + " ")[1]

            # Save Credentials
            CLIENT_DATA["PASS"] = passwd
            # Validate Credentials
            if CLIENT_DATA["USER"] == SERVER_DATA["USER"] and CLIENT_DATA["PASS"] == SERVER_DATA["PASS"]:
                # Auth success
                CLIENT_DATA["AUTHENTICATED"] = True

                response = "230 Login successful.\r\n"
                reply_cmd(client_connection, response)
            else:
                #Auth failed
                response = "530 Login incorrect.\r\n"
                reply_cmd(client_connection, response)

        elif "SYST" == cmd[0]:
            response = "215 UNIX emulated by FP.\r\n"
            reply_cmd(client_connection, response)
        elif "FEAT" == cmd[0]:
            response = "211-Features:\r\n SIZE\r\n211 End\r\n"
            reply_cmd(client_connection, response)
        elif "PWD" == cmd[0]: # This is authenticated
            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue

            response = "257 \"" + CLIENT_DATA["WD"] + "\" is current directory.\r\n"
            reply_cmd(client_connection, response)
        elif "CWD" == cmd[0]: # This command need an argument, authenticated
            if cmd[0] + " " in request == False:
                response = "501 Missing required argument\r\n"
                reply_cmd(client_connection, response)
                continue     

            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue
            
            request_wd = request.split(cmd[0] + " ")[1]

            # Then Validate Request WD
            real_wd = CLIENT_DATA["REAL_WD"]
            ftp_wd = CLIENT_DATA["WD"]

            request_wd_join = ""
            if request_wd[0] != "/":
                # append to ftp wd
                request_wd_join = f"{real_wd}{ftp_wd}{request_wd}"
            else:
                request_wd_join = f"{real_wd}{request_wd}"

            if os.path.exists(request_wd_join) == True and os.path.isfile(request_wd_join) == False:
                CLIENT_DATA["WD"] = request_wd

                # Fix naming
                if CLIENT_DATA["WD"][-1] != "/":
                    CLIENT_DATA["WD"] += "/"

                reply_cmd(client_connection, "250 CWD command successful\r\n")
                print("CWD sekarang", CLIENT_DATA["WD"])
            else:
                response = "550 Couldn't open the file or directory\r\n"
                reply_cmd(client_connection, response)
        elif "CDUP" == cmd[0]:
            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue
            
            response = "501 Missing required argument\r\n"
            reply_cmd(client_connection, response)
            
        elif "TYPE" == cmd[0]: # This command need an argument, authenticated
            if cmd[0] + " " in request == False:
                response = "501 Missing required argument\r\n"
                reply_cmd(client_connection, response)
                continue

            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue
            
            cmd_1 = request.split(cmd[0] + " ")[1]
            response = "200 Type set to "+cmd_1+"\r\n"
            reply_cmd(client_connection, response)
        elif "PASV" == cmd[0]: # Authenticated
            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue

            # Do some magic
            # Create new Socket Connection as Data Socket
            # data_port = p1 * 256 + p2, P1 < 256
            
            data_port = randint(1,2**16)
            while is_address_exist("127.0.0.1", data_port):
                data_port = randint(1,2**16)

            p1 = CLIENT_DATA["DATA_SOCK"]["P1"] = int(data_port/256)
            p2 = CLIENT_DATA["DATA_SOCK"]["P2"] = data_port % 256
            
            # Prepare Data Socket
            CLIENT_DATA["DATA_SOCKET"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CLIENT_DATA["DATA_SOCKET"].bind(("127.0.0.1", data_port))
            CLIENT_DATA["DATA_SOCKET"].listen(1)

            # Set PASV mode
            CLIENT_DATA["PASV"] = True

            response = f"227 Entering Passive Mode (127,0,0,1,{p1},{p2})\r\n"
            reply_cmd(client_connection, response)
        elif "LIST" == cmd[0]: # Authenticated
            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue

            # List ini harus PASV dulu
            # Check if PASV mode active
            if CLIENT_DATA["PASV"]:
                reply_cmd(client_connection, f"150 Starting data transfer.\r\n")

                # Accept Client from Data Socket
                DATA_SOCKET_CONN, datasoc_address = CLIENT_DATA["DATA_SOCKET"].accept()
                print(f"[+] Someone {datasoc_address} is connected to data socket.")

                # Response List
                real_wd = CLIENT_DATA["REAL_WD"]
                ftp_wd = CLIENT_DATA["WD"]
                output_exec = subprocess.run(['ls', '-l', f"{real_wd}{ftp_wd}"], capture_output=True, text=True).stdout
                list_dir = output_exec.split("\n")
                list_dir_str = "\r\n".join(list_dir[1:])

                print("Sending", list_dir_str)
                DATA_SOCKET_CONN.sendall(list_dir_str.encode())
                DATA_SOCKET_CONN.close()

                # Disable PASV mode
                CLIENT_DATA["PASV"] = False

                reply_cmd(client_connection, f"226 Operation successful\r\n")
            else:
                # Send Error Message
                reply_cmd(client_connection, f"425 Use PORT or PASV first.\r\n")
        elif "MKD" == cmd[0]: # Authenticated, Need argument
            if cmd[0] + " " in request == False:
                response = "501 Missing required argument\r\n"
                reply_cmd(client_connection, response)
                continue

            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue
            
            dir_name = request.split(cmd[0] + " ")[1]
            # try catch
            try:
                real_wd = CLIENT_DATA["REAL_WD"]
                ftp_wd = CLIENT_DATA["WD"]
                os.mkdir(f"{real_wd}{ftp_wd}{dir_name}")

                # Success then resp
                response = f"257 \"{ftp_wd}{dir_name}\" created successfully.\r\n"
                reply_cmd(client_connection, response)
            except Exception as ex:
                response = "550 Failed to create folder.\r\n"
                reply_cmd(client_connection, response)
        elif "RMD" == cmd[0]: # Authenticated, Need argument
            if cmd[0] + " " in request == False:
                response = "501 Missing required argument\r\n"
                reply_cmd(client_connection, response)
                continue

            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue
            
            dir_name = request.split(cmd[0] + " ")[1]
            # try catch
            try:
                real_wd = CLIENT_DATA["REAL_WD"]
                ftp_wd = CLIENT_DATA["WD"]
                shutil.rmtree(f"{real_wd}{ftp_wd}{dir_name}")

                # Success then resp
                response = f"250 Directory deleted successfully.\r\n"
                reply_cmd(client_connection, response)
            except Exception as ex:
                response = "550 Failed to delete folder.\r\n"
                reply_cmd(client_connection, response)

        elif "DELE" == cmd[0]: # Authenticated, Need argument
            if cmd[0] + " " in request == False:
                response = "501 Missing required argument\r\n"
                reply_cmd(client_connection, response)
                continue

            if CLIENT_DATA["AUTHENTICATED"] == False:
                response = "530 Please log in with USER and PASS first.\r\n"
                reply_cmd(client_connection, response)
                continue
            
            file_name = request.split(cmd[0] + " ")[1]
            # try catch
            try:
                real_wd = CLIENT_DATA["REAL_WD"]
                ftp_wd = CLIENT_DATA["WD"]
                os.remove(f"{real_wd}{ftp_wd}{file_name}")

                # Success then resp
                response = f"250 File deleted successfully.\r\n"
                reply_cmd(client_connection, response)
            except Exception as ex:
                response = "550 Failed to delete file.\r\n"
                reply_cmd(client_connection, response)
        elif "HELP" == cmd[0]:
            response = "214 The following commands are recognized.\r\n"

            for i in range(0,len(LIST_COMMAND)):
                response += LIST_COMMAND[i] + " "
                if (i + 1) % 10 == 0:
                    response = response[:-1] + "\r\n"
            
            response += "\r\n214 Help ok.\r\n"
            reply_cmd(client_connection, response)
        elif "QUIT" == cmd[0]:
            reply_cmd(client_connection, "200 Goodbye.\r\n")
            break

    # Close connection
    client_connection.close()

try:
    client_connection, client_address = server_socket.accept()
    print(f"[+] New client {client_address} is connected.")

    threaded_socket(client_connection)
        
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)