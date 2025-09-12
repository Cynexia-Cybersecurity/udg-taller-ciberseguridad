# udg-taller-ciberseguridad

## Deploy
```bash
MY_USER=cynexia

sudo apt-get install authbind git
sudo touch /etc/authbind/byport/502
sudo chown $MY_USER:$MY_USER /etc/authbind/byport/502
sudo chmod 770 /etc/authbind/byport/502

git clone https://github.com/Cynexia-Cybersecurity/udg-taller-ciberseguridad.git
cd udg-taller-ciberseguridad
python3 -m venv venv
source venv/bin/activate
```

```bash
mkdir -p ~/.config/systemd/user &&\
nano ~/.config/systemd/user/modbus-server.service
```

```txt
[Unit]
Description=Modbus Server Service
After=network.target

[Service]
ExecStart=/usr/bin/authbind --deep /home/cynexia/udg-taller-ciberseguridad/modbus/venv/bin/python3 /home/cynexia/udg-taller-ciberseguridad/modbus/server.py
WorkingDirectory=/home/cynexia/udg-taller-ciberseguridad/modbus
Restart=always
Environment="PATH=/home/cynexia/udg-taller-ciberseguridad/modbus/venv/bin"

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now modbus-server.service
systemctl --user status modbus-server.service
```
