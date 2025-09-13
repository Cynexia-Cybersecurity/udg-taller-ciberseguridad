# Servidor OPC UA de Sensores Simulados

Este proyecto es un servidor OPC UA para fines **puramente educativos**. Simula la lectura de datos de sensores para demostrar cómo implementar un servidor OPC UA básico con autenticación y seguridad en la comunicación.

**ADVERTENCIA**: Este código no debe ser utilizado en un entorno de producción. La autenticación y la gestión de la seguridad implementadas son básicas y están diseñadas solo para la enseñanza.

## Funcionalidades
-   Servidor OPC UA con datos simulados de nivel de agua, cloro residual y presión de válvula.
-   Autenticación de usuario y contraseña (usuario `admin`, contraseña `admin`).
-   Comunicación cifrada mediante certificados de seguridad.

## Cómo ejecutar el proyecto

### 1. Requisitos
Asegúrate de tener Python 3 y un entorno virtual configurado. Instala las librerías necesarias:
```bash
sudo apt-get install build-essential libffi-dev python3-dev
pip install -r requirements.txt
```

### 2. Generar Certificados de Seguridad
La comunicación cifrada requiere un certificado y una clave privada. Si no los tienes, puedes generarlos de forma segura y manual usando OpenSSL, que está preinstalado en la mayoría de los sistemas Linux.

Ejecuta los siguientes comandos en la terminal en la raíz de tu proyecto:
```bash
openssl genpkey -algorithm rsa -out private_key.pem
openssl req -new -x509 -key private_key.pem -out cert.der -days 365
```

### 3. Ejecutar el Servidor
Una vez que tengas los archivos private_key.pem y cert.der en el mismo directorio que tu script, puedes iniciar el servidor:

```bash
python3 server.py
```

### 4. Ejecutar en Background como servicio

```bash
mkdir -p ~/.config/systemd/user &&\
nano ~/.config/systemd/user/opcua-server.service
```


```txt
[Unit]
Description=opcua Server Service
After=network.target

[Service]
ExecStart=/usr/bin/authbind --deep /home/cynexia/udg-taller-ciberseguridad/opcua/venv/bin/python3 /home/cynexia/udg-taller-ciberseguridad/opcua/server.py
WorkingDirectory=/home/cynexia/udg-taller-ciberseguridad/opcua
Restart=always
Environment="PATH=/home/cynexia/udg-taller-ciberseguridad/opcua/venv/bin"

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now opcua-server.service
systemctl --user status opcua-server.service
```
