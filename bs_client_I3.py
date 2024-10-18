import socket
from sys import exit
from re import search

host = '10.1.1.1'
port = 13337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
    msg = input("Que veux-tu envoyer au serveur : ")
    if type(msg) is not str:
        raise TypeError("Ici on veut que des strings !")
    if search(".*meow.*", msg) or search(".*waf.*", msg):
        s.sendall(msg.encode())
        data = s.recv(1024)
        s.close()
        print(f"Le serveur a répondu {repr(data)}")
    else:
        raise TypeError("Ici on veut que des strings !")
except Exception as e:
    print("On dirait qu'il y a eu un soucis, déso.")
    print(f"L'erreur native est : {e}")
exit(0)