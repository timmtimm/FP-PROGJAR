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

BUFFER_SIZE=1024
# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6999

SERVER_DATA = {
    "USER" : "ariesta",
    "PASS" : "password"
}

CLIENT_DATA = {
    "USER" : None,
    "PASS" : None,
    "AUTHENTICATED" : False,
    "ENCODING": "ASCII",
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

        request = request.rstrip()
        cmd = request.split(" ")
        print("Command", cmd[0])

        # Check if PASV mode active
        if CLIENT_DATA["PASV"]:
            # Accept Client from Data Socket
            CLIENT_DATA["DATA_SOCKET_CONN"], datasoc_address = CLIENT_DATA["DATA_SOCKET"].accept()
            print(f"[+] Someone {datasoc_address} is connected to data socket.")

            # Disable PASV mode
            CLIENT_DATA["PASV"] = False

        if "AUTH" in cmd[0]:
            client_connection.sendall("234 Using authentication type TLS.\r\n".encode())
        elif "USER" in cmd[0]:
            client_connection.sendall("331 Please, specify the password.\r\n".encode())
            CLIENT_DATA["USER"] = request.split(cmd[0] + " ")[1]
        elif "PASS" in cmd[0]:
            CLIENT_DATA["PASS"] = request.split(cmd[0] + " ")[1]
            
            # Validate Credentials
            if CLIENT_DATA["USER"] == SERVER_DATA["USER"] and CLIENT_DATA["PASS"] == SERVER_DATA["PASS"]:
                # Auth success
                client_connection.sendall("230 Login successful.\r\n".encode())
            else:
                #Auth failed
                client_connection.sendall("530 Login incorrect.\r\n".encode())
        elif "SYST" in cmd[0]:
            client_connection.sendall("215 UNIX emulated by FP.\r\n".encode())
        elif "FEAT" in cmd[0]:
            client_connection.sendall("211 SP.\r\n".encode())
        elif "PWD" in cmd[0]:
            response = "257 \"" + CLIENT_DATA["WD"] + "\" is current directory.\r\n"
            client_connection.sendall(response.encode())
        elif "TYPE" in cmd[0]:
            if "I" in cmd[1]:
                response = "200 Type set to "+cmd[1]+"\r\n"
                client_connection.sendall(response.encode())
            else:
                response = "200 Type set to "+cmd[1]+"\r\n"
                client_connection.sendall(response.encode())
        elif "PASV" in cmd[0]:
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
            print(response, data_port)            
            client_connection.sendall(response.encode())
        elif "LIST" in cmd[0]:
            response = f"150 Starting data transfer.\r\n"
            print(response)
            client_connection.sendall(response.encode())

            # Response List
            response = f"-rw-rw-rw- 1 ftp ftp               0 Apr 26 07:07 aaa.txt\r\n"
            print("Sending", response)
            CLIENT_DATA["DATA_SOCKET_CONN"].sendall(response.encode())
        elif "EXIT" in cmd[0]:
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