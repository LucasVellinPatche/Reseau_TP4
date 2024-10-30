from psutil import net_if_addrs
import socket
from re import search
import argparse
from os import path, mkdir
import logging

LOG_FILE = "/var/log/server_tp4/server.log"

if path.isdir("/var/log/server_tp4") != True:
    mkdir("/var/log/server_tp4")

if path.isfile(LOG_FILE) != True:
    log = open(LOG_FILE, "x")

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M", format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8", filemode="a")
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def_args = argparse.ArgumentParser()
def_args.add_argument("-p", "--port", type=int, choices=range(1024, 65535), nargs="?", default=13337, help="take the listenning port", metavar='')
def_args.add_argument("-l", "--listen", type=str, nargs="?", default="localhost", help="take the serveur ip to listen")


arg = def_args.parse_args()
port = arg.port
host = arg.listen

if search("[0-9]?[0-9]?[0-9][.][0-9]?[0-9]?[0-9][.][0-9]?[0-9]?[0-9][.][0-9]?[0-9]?[0-9]", host):
    ip_number = ""
    for byte in host.split("."):
        section_ip = int(byte)
        if (section_ip < 255) == False:
            raise ValueError(f"ERROR -l argument invalide. L'adresse {host} n'est pas une adresse IP valide.")
else:
    raise ValueError(f"ERROR -l argument invalide. L'adresse {host} n'est pas une adresse IP valide.")

trouve = 0
trop_de_trucs = []
trop_de_trucs = net_if_addrs()
for i in trop_de_trucs:
    x = 0
    for n in trop_de_trucs[i]:
        if trop_de_trucs[i][x].family == 2:
            if trop_de_trucs[i][x].address == host:
                trouve = 1
        x += 1
if trouve != 1:
    raise ValueError(f"ERROR -l argument invalide. L'adresse {host} n'est pas l'une des adresses IP de cette machine.")

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
        if search(".*meo.*", str(data)):
            conn.sendall(b"Meo a toi confrere.")
        elif search(".*waf.*", str(data)):
            conn.sendall(b"ptdr t ki")
        else:
            conn.sendall(b"Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

conn.close()
exit(0)

#exit(1)
#exit(2)