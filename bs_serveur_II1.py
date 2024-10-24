import socket
from re import search
import argparse

def_args_host = argparse.ArgumentParser()
def_args_host.add_argument("-l", "--listen", type=str, nargs="?", default="localhost")
def_args_port = argparse.ArgumentParser()
def_args_port.add_argument("-p", "--port", type=int, choices=range(1024, 65535), nargs="?", default=13337)

host = def_args_host.parse_args
try:
    search("[0-9]?[0-9]?[0-9][.][0-9]?[0-9]?[0-9][.][0-9]?[0-9]?[0-9][.][0-9]?[0-9]?[0-9]", host)
    ip_number = ""
    for byte in host.split("."):
        section_ip = int(byte)
        try:
            (section_ip < 255)
        except:
            raise ValueError(f"ERROR -l argument invalide. L'adresse {host} n'est pas une adresse IP valide.")
except:
    raise ValueError(f"ERROR -l argument invalide. L'adresse {host} n'est pas une adresse IP valide.")

try:
    port = def_args_port.parse_args
except:
    if (def_args_port.parse_args < 0) or (def_args_port.parse_args > 65535):
        raise ValueError(f"ERROR -p argument invalide. Le port spécifié {def_args_port.parse_args} n'est pas un port valide (de 0 à 65535).")
    elif def_args_port.parse_args < 1025:
        raise ValueError(f"ERROR -p argument invalide. Le port spécifié {def_args_port.parse_args} est un port privilégié. Spécifiez un port au dessus de 1024.")
    else:
        raise TypeError("Le paramètre rentré en port n'est pas valide !")

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
exit(0)

#exit(1)
#exit(2)