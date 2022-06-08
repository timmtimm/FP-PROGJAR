import socket
import time

print("Welcome to FTP clientnan")

HOST = input("enter server:")
PORT = int(input("enter port:"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(1.0)

DATA_SOCK = None
BUFFER_SIZE=4096

# DATA SOCK
RETR = None
STOR = None
PASV = -1
CLIENT_WD = "/mnt/c/code/PROGJAR/FP-PROGJAR"

def parse_resp(msg):
    resp_code = msg[:3]
    resp_msg = msg[4:]
    return resp_code, resp_msg

while True:
    print("[>] SEND :", end="")
    cmd = input()
    print(cmd)
    s.send(f"{cmd}\r\n".encode())

    if PASV == 0:
        PASV += 1

    if "RETR " == cmd[:5]:
        RETR = cmd[5:]

    if "STOR " == cmd[:5]:
        STOR = cmd[5:]

    # Always waiting all response from FTP Sock
    while True:
        try:
            resp = s.recv(BUFFER_SIZE).decode()
            if len(resp) == 0:
                break
        except Exception as ex:
            break

        print("[<] RESP :", resp)
        code,msg = parse_resp(resp.strip())
        # print(code, msg)

        if "Entering Passive Mode" in msg:
            # print("Connecting to passive mode")
            datas = msg.strip().split("(")[1].split(")")[0].split(",")
            p1,p2 = int(datas[-2]), int(datas[-1])
            data_port = p1 * 256 + p2

            DATA_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DATA_SOCK.settimeout(1.0)
            DATA_SOCK.connect(('localhost', data_port))
            PASV = 0

    # Sending STOR
    if PASV > 0 and STOR != None:
        # print("SENDING FILES")
        with open(f"{CLIENT_WD}/{STOR}", "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                # print(bytes_read)
                if len(bytes_read) == 0:
                    break
                DATA_SOCK.sendall(bytes_read)
        print("SENDING FILES DONE, sleep 2 sec")
        time.sleep(2)
        print("DONE, Closing socket now")
        DATA_SOCK.close()
        STOR = None
        PASV = -1

    # Also waiting all response from DataSock if available
    datasock_resp = ""
    if PASV > 0:
        if RETR != None:
            with open(f"{CLIENT_WD}/DOWNLOAD/{RETR}", "wb") as f:
                while True:
                    bytes_recv = DATA_SOCK.recv(4096)
                    if len(bytes_recv) == 0:
                        break

                    f.write(bytes_recv)
                f.close()
            DATA_SOCK.close()
            RETR = None
        else:
            print("OK")
            datasock_resp = ""
            while True:
                try:
                    resp = DATA_SOCK.recv(4096).decode().rstrip()
                    if len(resp) == 0:
                        DATA_SOCK.close()
                        break

                    datasock_resp += resp
                except Exception as ex:
                    DATA_SOCK.close()
                    break
            
            print(datasock_resp)
        
        PASV = -1

    if cmd == "QUIT":
        break
    
print("Thank you for using FTP clientnan")