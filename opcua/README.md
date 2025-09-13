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
pip install opcua cryptography
```

### 2. Generar Certificados de Seguridad
La comunicación cifrada requiere un certificado y una clave privada. Si no los tienes, puedes generarlos de forma segura y manual usando OpenSSL, que está preinstalado en la mayoría de los sistemas Linux.

Ejecuta los siguientes comandos en la terminal en la raíz de tu proyecto:
```bash
openssl genrsa -out private_key.pem 2048
openssl req -new -x509 -key private_key.pem -out cert.der -days 365
```

### 3. Ejecutar el Servidor
Una vez que tengas los archivos private_key.pem y cert.der en el mismo directorio que tu script, puedes iniciar el servidor:

```bash
python3 server.py
```

