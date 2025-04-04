import socket
from _thread import *
import sys
import threading  # Pre zámky (locks)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.88.11'
port = 11000

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

# Zámok na synchronizáciu prístupu k "pos"
lock = threading.Lock()

# Inicializácia ID a pozícií
currentId = 0  # Ak by si chcel dynamicky priraďovať ID
pos = ["0:50,50", "1:100,100"]


def threaded_client(conn):
    global currentId, pos
    lock.acquire()
    clientId = currentId
    currentId += 1
    lock.release()

    conn.send(str.encode(str(clientId)))

    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print("No data received, closing connection")
                break  # Koniec komunikácie

            reply = data.decode('utf-8')
            print(f"Received: {reply}")

            arr = reply.split(":")
            id = int(arr[0])
            pos[id] = reply

            nid = 1 if id == 0 else 0
            reply = pos[nid]
            print(f"Sending: {reply}")

            conn.sendall(str.encode(reply))  # Posielanie dát klientovi
        except socket.error as e:
            print(f"Socket error: {e}")
            break  # V prípade chyby prerušíme komunikáciu

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Spustenie nového vlákna pre každý klienta
    start_new_thread(threaded_client, (conn,))
