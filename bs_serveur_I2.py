import socket
from re import search

host = '10.1.1.1'
port = 13337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  
s.listen(1)
conn, addr = s.accept()

while True:

    try:
        data = conn.recv(1024)
        if not data: break
        print(f"Un client vient de se co et son IP c'est {addr[0]}.")
        print(f"Données reçues du client : {data}")
        if search(".*meow.*", str(data)):
            conn.sendall(b"Meo a toi confrere.")
        elif search(".*waf.*", str(data)):
            conn.sendall(b"ptdr t ki")
        else:
            conn.sendall(b"Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

conn.close()
