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
        logging.INFO: format,
        logging.ERROR: red + format + nc
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger(__name__)
logger.setLevel(10)
console_handler = logging.StreamHandler()
console_handler.setLevel(40)
console_handler.setFormatter(CustomFormatter())
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(10)
file_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)
logger.addHandler(file_handler)

host = '10.1.1.1'
port = 13337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    logger.info(f"Connexion réussie à {host}:{port}.")
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
    msg = input("Que veux-tu envoyer au serveur : ")
    if type(msg) is not str:
        raise TypeError("Ici on veut que des strings !")
    if search(".*meow.*", msg) or search(".*waf.*", msg):
        s.sendall(msg.encode())
        logger.info(f"Message envoyé au serveur {host} : {msg}.")
        data = s.recv(1024)
        s.close()
        print(f"Le serveur a répondu {repr(data.decode())}")
        logger.info(f"Réponse reçue du serveur {host} : {data.decode()}.")
    else:
        raise ValueError("Ici on veut du félin #meow !(ou on tolère les chiens #waf)")
except Exception as e:
    print("On dirait qu'il y a eu un soucis, déso.")
    print(f"L'erreur native est : {e}")
    logger.error(f"Impossible de se connecter au serveur {host} sur le port {port}")
    
exit(0)