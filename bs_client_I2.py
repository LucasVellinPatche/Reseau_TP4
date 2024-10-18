import socket
from sys import exit

host = '10.1.1.1'
port = 13337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
    s.sendall(input("Que veux-tu envoyer au serveur : ").encode())
    data = s.recv(1024)
    s.close()
    print(f"Le serveur a répondu {repr(data)}")
except Exception as e:
    print("On dirait qu'il y a eu un soucis, déso.")
    print(f"L'erreur native est : {e}")
exit(0)