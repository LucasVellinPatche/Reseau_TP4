import socket
from sys import exit
from re import search
import logging

LOG_FILE = "/var/log/bs_client/bs_client.log"

class CustomFormatter(logging.Formatter):
    red = "\x1b[31;20m"
    nc = "\x1b[0m"
    format = "%(asctime)s %(levelname)s %(message)s"

    FORMATS = {
        logging.ERROR: red + format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logging.basicConfig(level=logging.WARN, datefmt="%Y-%m-%d %H:%M", format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
logger.addHandler(console_handler)
logger.addHandler(file_handler)

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
        raise ValueError("Ici on veut du félin #meow !(ou on tolère les chiens #waf)")
except Exception as e:
    print("On dirait qu'il y a eu un soucis, déso.")
    print(f"L'erreur native est : {e}")
    logger.error(f"Impossible de se connecter au serveur {host} sur le port {port}")
    
exit(0)