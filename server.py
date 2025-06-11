import socket
from _thread import *
import time

# Boost management
boosts = []  # Shared boost positions and types
taken_boost_ids = set()  # To keep track of used boosts

# Add this if using custom boost sync
def generate_boosts():
    return [
        "heal:600,300",
        "shield:800,500",
        "turbo:1000,400"
    ]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "192.168.10.53"
port = 11000
server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50,0||50", "1:100,100,0||50"]

def threaded_client(conn, player_id):
    global currentId, pos, boosts, taken_boost_ids

    conn.send(str.encode(str(player_id)))
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                break

            reply = data.decode("utf-8")
            if reply.startswith("BOOST_TAKEN:"):
                boost_id = reply.split(":")[1]
                taken_boost_ids.add(boost_id)
                continue

            arr = reply.split(":")
            id = int(arr[0])
            pos[id] = reply

            nid = 1 - id
            response = f"{pos[nid]}~{';'.join(boosts)}~{','.join(taken_boost_ids)}"
            conn.sendall(str.encode(response))
        except:
            break

    print("Connection Closed")
    conn.close()

# Prepare shared boost data before game starts
boosts = generate_boosts()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, int(currentId)))
    currentId = str(1 - int(currentId))