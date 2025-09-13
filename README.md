# udg-taller-ciberseguridad

## Encontrando dispositivos en la red
```bash
netdiscover -i wlp2s0 -r 192.168.1.0/24
netdiscover -i wlp2s0 -p
sudo arp-scan -I wlp2s0 --localnet
```

## MITM

`sudo go/bin/bettercap -iface wlp2s0`
| Orden | Descripción |
|-------|---------|
| net.show | Mostrar información sobre la red |
| net.probe on | Iniciar escaneo de host en la red |
| net.recon | Leer periódicamente la tabla ARP del sistema para detectar nuevos hosts en la red. |
| set arp.spoof.targets 192.168.100.100,192.168.100.200 | Establecer un objetivo en la red |
