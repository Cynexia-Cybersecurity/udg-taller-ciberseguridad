#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
from opcua import Server, ua
from struct import unpack_from



use_crypto = True
try:
    from opcua.crypto import uacrypto
except ImportError:
    use_crypto = False

class UserManager(object):
    def __init__(self, private_key):
        
        assert(hasattr(private_key, 'private_bytes'))
        
        self.private_key = private_key

        self.users = {
            "admin": "admin",
        }

    def check_user_token(self, isession, token):
        userName = token.UserName
        passwd = token.Password

        # decrypt password is we can
        if str(token.EncryptionAlgorithm) != "None":
            if use_crypto == False:
                return False
            try:
                if token.EncryptionAlgorithm == "http://www.w3.org/2001/04/xmlenc#rsa-1_5":
                    raw_pw = uacrypto.decrypt_rsa15(self.private_key, passwd)
                elif token.EncryptionAlgorithm == "http://www.w3.org/2001/04/xmlenc#rsa-oaep":
                    raw_pw = uacrypto.decrypt_rsa_oaep(self.private_key, passwd)
                else:
                    print("Unknown password encoding '{0}'".format(token.EncryptionAlgorithm))
                    return False
                length = unpack_from('<I', raw_pw)[0] - len(isession.nonce)
                passwd = raw_pw[4:4 + length]
                passwd = passwd.decode('utf-8')
            except Exception as exp:
                print("Unable to decrypt password")
                return False
        else:
            try:
                passwd = passwd.decode('utf-8')
            except:
                print("Unable to decode password")

        return userName in self.users and self.users[userName] == passwd


def main():
    try:
        server = Server()
        server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

        # --- CONFIGURACIÓN DE SEGURIDAD ---
        server.load_certificate("cert.der")
        server.load_private_key("private_key.pem")

        server.set_security_policy([
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt
        ])

        # --- FIN DE LA CONFIGURACIÓN ---

        server.set_server_name("Simulated OPC UA Server")
        idx = server.register_namespace("http://lab.local/opcua/simulated_sensors")

        # Configurar autenticación
        server.set_security_IDs(["Username"])
        server.user_manager = UserManager(private_key=server.private_key)

        objects = server.get_objects_node()
        sensor_obj = objects.add_object(idx, "SensorValues")

        # Add variables
        water_level = sensor_obj.add_variable(idx, "WaterLevelPercent", 0)
        chlorine_residual = sensor_obj.add_variable(idx, "ChlorineResidual", 0)
        valve_pressure = sensor_obj.add_variable(idx, "ValvePressurePsi", 0)

        # Set allow writting (optional)
        # water_level.set_writable()
        # chlorine_residual.set_writable()
        # valve_pressure.set_writable()

        server.start()
        print("Servidor OPC UA iniciado en opc.tcp://0.0.0.0:4840")
        print("Sirviendo los siguientes valores simulados:")
        print("- Nivel de agua (%): 60–70")
        print("- Cloro residual (mg/L ×100): 1000–1500")
        print("- Presión válvula (psi): 30–50")

        while True:
            # Generar valores aleatorios
            wl = random.randint(60, 70)
            cl = random.randint(1000, 1500)
            vp = random.randint(30, 50)

            # Asignar valores
            water_level.set_value(wl)
            chlorine_residual.set_value(cl)
            valve_pressure.set_value(vp)

            # Debug opcional
            # print(f"[{datetime.now()}] Water Level: {wl}%, Chlorine: {cl / 100:.2f} mg/L, Pressure: {vp} psi")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        server.stop()
        print("Servidor OPC UA detenido.")


if __name__ == "__main__":
    main()
