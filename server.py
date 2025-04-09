import socket

# Vytvorenie UDP socketu
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = '127.0.0.1'
port = 11000

try:
    s.bind((server, port))
    print("UDP Server spustený na porte", port)
except socket.error as e:
    print(str(e))
    exit()

# Počiatočné pozície hráčov
pos = {
    "0": "0:50,50",
    "1": "1:100,100"
}

# Mapovanie adries na ID (voliteľné)
addr_to_id = {}
next_id = 0

while True:
    try:
        data, addr = s.recvfrom(2048)
        msg = data.decode('utf-8')

        # Priradenie ID podľa adresy
        if addr not in addr_to_id:
            addr_to_id[addr] = str(next_id)
            print(f"Priradené ID {next_id} pre klienta {addr}")
            next_id += 1

        current_id = addr_to_id[addr]

        # Ak klient pošle len prázdnu správu, pošleme mu jeho ID
        if msg == "get_id":
            s.sendto(current_id.encode(), addr)
            continue

        # Uloženie pozície klienta
        arr = msg.split(":")
        if len(arr) == 2:
            player_id = arr[0]
            pos[player_id] = msg

        # Získaj ID druhého hráča
        other_id = "1" if current_id == "0" else "0"
        reply = pos.get(other_id, "no_data")

        print(f"[{addr}] {msg} -> {reply}")
        s.sendto(reply.encode(), addr)

    except Exception as e:
        print("Chyba:", e)
