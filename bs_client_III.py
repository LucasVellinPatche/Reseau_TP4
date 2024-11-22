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
except:
    logger.error(f"Impossible de se connecter au serveur {host} sur le port {port}")

try:
    msg = input("Time to calculate, fait péter l'opération ! : ")
    if search("[a-z]",msg):
        raise ValueError("Bah alors, on a mis des lettres ?")
    elif search("/",msg):
        raise ValueError("Pas de divisions mon petit pote, déso")
    for num in msg.split("+|-|*"):
        if int(num) < -100000 or int(num) > 100000:
            raise ValueError("Il faut des valeurs comprises entre -100000 et +100000")
except Exception as e:
    print("On dirait qu'il y a eu un soucis, déso.")
    print(f"L'erreur native est : {e}")
    
    
exit(0)