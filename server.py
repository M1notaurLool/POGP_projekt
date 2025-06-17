import socket
from _thread import *
import sys

# Get IP and port from command-line arguments
if len(sys.argv) != 3:
    print("Usage: server.py <ip> <port>")
    sys.exit(1)

server = sys.argv[1]
port = int(sys.argv[2])

# Boost management
boosts = []
taken_boost_ids = set()

def generate_boosts():
    return [
        "heal:600,300",
        "shield:800,500",
        "turbo:1000,400"
    ]

# Create and bind socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(f"Bind failed: {e}")
    sys.exit(1)

s.listen(2)
print(f"Server started at {server}:{port}, waiting for connection...")

currentId = "0"
pos = ["0:50,50,0||50", "1:100,100,0||50"]

def threaded_client(conn, player_id):
    global currentId, pos, boosts, taken_boost_ids

    conn.send(str.encode(str(player_id)))
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

boosts = generate_boosts()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, int(currentId)))
    currentId = str(1 - int(currentId))
