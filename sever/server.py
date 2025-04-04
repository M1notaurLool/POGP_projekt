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
    # Priraď ID klientovi
    lock.acquire()  # Uzamkneme, aby sme zabezpečili, že len jeden klient dostane ID
    clientId = currentId
    currentId += 1
    lock.release()

    conn.send(str.encode(str(clientId)))

    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print(f"Received: {reply}")
                arr = reply.split(":")
                id = int(arr[0])  # Klient ID
                pos[id] = reply  # Aktualizácia pozície

                # Zistenie id druhého klienta
                nid = 1 if id == 0 else 0

                reply = pos[nid][:]  # Pošleme pozíciu druhého klienta
                print(f"Sending: {reply}")

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Spustenie nového vlákna pre každý klienta
    start_new_thread(threaded_client, (conn,))
