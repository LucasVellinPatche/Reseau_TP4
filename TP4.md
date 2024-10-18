# RenduTP4

## PI1

### Commandes coté serveur

```
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=13337/tcp
sudo firewall-cmd --add-port=13337/tcp --permanent
python bs_serveur_I1.py
```

### Commande coté client

```
python bs_client_I1.py
```

### Commande lnpt

```
ss -lnpt | grep 13337
LISTEN 0      1           10.1.1.1:13337      0.0.0.0:*    users:(("python",pid=3125,fd=3))
```