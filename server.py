import socket

server = '192.168.88.11'
port = 11000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.bind((server, port))
    print("[SERVER] UDP Server spustený na porte", port)
except socket.error as e:
    print("[SERVER] Chyba:", str(e))
    exit()

# Ukladanie pozícií hráčov – predvolené pozície pre hráčov 0 a 1.
pos = {
    "0": "0:50,50",
    "1": "1:100,100"
}

addr_to_id = {}
next_id = 0

while True:
    try:
        data, addr = s.recvfrom(2048)
        msg = data.decode('utf-8')

        # Ak je klient nový, priraď mu unikátne ID.
        if addr not in addr_to_id:
            addr_to_id[addr] = str(next_id)
            print(f"[SERVER] Priradené ID {next_id} pre klienta {addr}")
            next_id += 1

        current_id = addr_to_id[addr]

        # Ak klient požiada o svoje ID, odpíš mu ho.
        if msg == "get_id":
            s.sendto(current_id.encode(), addr)
            continue

        # Aktualizácia pozície hráča podľa prijatej správy.
        arr = msg.split(":")
        if len(arr) == 2:
            player_id = arr[0]
            pos[player_id] = msg  # formát správy: "ID:x,y"

        # Získaj pozíciu súperového hráča.
        other_id = "1" if current_id == "0" else "0"
        reply = pos.get(other_id, "no_data")

        # Debugging: vypíš odosielané údaje.
        print(f"[SERVER] Posielam hráčovi {current_id} pozíciu: {reply}")
        s.sendto(reply.encode(), addr)

    except Exception as e:
        print("[SERVER] Chyba:", e)
