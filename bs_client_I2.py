import socket
from sys import exit

host = '10.1.1.1'
port = 13337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
except:
    print("Ça marche pas chef, ça se co pas, déso.")
msg = input("Que veux-tu envoyer au serveur : ")
s.sendall(b'' + msg)
data = s.recv(1024)
s.close()
print(f"Le serveur a répondu {repr(data)}")
exit(0)