from psutil import net_if_addrs
import socket
from re import search
import argparse
from os import path, mkdir
import logging

LOG_FILE = "/var/log/bs_server/bs_server.log"

class CustomFormatter(logging.Formatter):
    white = "\e[97m"
    yellow = "\e[93m"
    nc = "\e[0m"
    time = "%(asctime)s"
    level = "%(levelname)s"
    msg = "%(message)s"

    FORMATS = {
        logging.INFO: time + white + level + nc + msg,
        logging.WARNING: time + yellow + level + nc + msg,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M", format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
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
logger.info(f"Le serveur tourne sur {host}:{port}")

try:
    s.timeout(1)
except:
    logger.warning("Aucun client depuis plus de une minute.")

conn, addr = s.accept()
logger.info(f"Un client {addr[0]} s'est connecté.")


while True:

    try:
        data = conn.recv(1024)
        data = data.decode
        if not data: break
        print(type(data))
        logger.info(f"Le client {addr[0]} a envoyé {data}.")
        if search(".*meo.*", data):
            conn.sendall(b"Meo a toi confrere.")
            logger.info(f"Réponse envoyée au client {addr[0]} : Meo a toi confrere.")
        elif search(".*waf.*", data):
            conn.sendall(b"ptdr t ki")
            logger.info(f"Réponse envoyée au client {addr[0]} : ptdr t ki")
        else:
            conn.sendall(b"Mes respects humble humain.")
            logger.info(f"Réponse envoyée au client {addr[0]} : Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

conn.close()
exit(0)

#exit(1)
#exit(2)