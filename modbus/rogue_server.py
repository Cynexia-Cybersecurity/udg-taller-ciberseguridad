#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Second Modbus TCP server that connects to the first one,
amplifies sensor values using a ROGUE_VARIABLE, and serves
the modified values through its own Modbus TCP server.
"""

import time
import modbus_tk
import modbus_tk.defines as defines
from modbus_tk import modbus_tcp


# =============================
# Configuración general
# =============================

# Variable de amplificación
ROGUE_VARIABLE = 1.25

# Parámetros de conexión al servidor original
SOURCE_SERVER_IP = '10.10.10.200'
SOURCE_SERVER_PORT = 502
SOURCE_SLAVE_ID = 1
SOURCE_START_ADDRESS = 0
SOURCE_NUM_REGISTERS = 3

# Parámetros del servidor amplificado
AMPLIFIED_SERVER_IP = '0.0.0.0'
AMPLIFIED_SERVER_PORT = 502  # Asegúrate de que esté libre
AMPLIFIED_SLAVE_ID = 1
AMPLIFIED_BLOCK_NAME = 'amplified_block'

# Intervalo de actualización en segundos
UPDATE_INTERVAL = 2

def main():
    """Crea el segundo servidor Modbus que amplifica los datos del primero."""
    try:
        # =============================
        # Conexión al primer servidor (cliente Modbus)
        # =============================
        print(f"Connecting to source Modbus server at {SOURCE_SERVER_IP}:{SOURCE_SERVER_PORT}...")
        source_client = modbus_tcp.TcpMaster(host=SOURCE_SERVER_IP, port=SOURCE_SERVER_PORT)
        source_client.set_timeout(5.0)
        print("Connected to source server.")

        # =============================
        # Crear el servidor Modbus propio (servidor TCP)
        # =============================
        print(f"Starting amplified Modbus server on {AMPLIFIED_SERVER_IP}:{AMPLIFIED_SERVER_PORT}...")
        amplified_server = modbus_tcp.TcpServer(address=AMPLIFIED_SERVER_IP, port=AMPLIFIED_SERVER_PORT)
        amplified_server.start()

        amplified_slave = amplified_server.add_slave(AMPLIFIED_SLAVE_ID)
        amplified_slave.add_block(
            AMPLIFIED_BLOCK_NAME,
            defines.HOLDING_REGISTERS,
            0,
            SOURCE_NUM_REGISTERS
        )

        print("Amplified server is running and ready to serve data.")

        while True:
            # =============================
            # Leer registros del primer servidor
            # =============================
            try:
                raw_values = source_client.execute(
                    SOURCE_SLAVE_ID,
                    defines.READ_HOLDING_REGISTERS,
                    SOURCE_START_ADDRESS,
                    SOURCE_NUM_REGISTERS
                )

                # =============================
                # Aplicar amplificación
                # =============================
                amplified_values = [int(value * ROGUE_VARIABLE) for value in raw_values]

                # =============================
                # Publicar en el segundo servidor
                # =============================
                amplified_slave.set_values(AMPLIFIED_BLOCK_NAME, 0, amplified_values)

                # =============================
                # Debug
                # =============================
                print(f"[Amplified] Original: {raw_values} -> Amplified: {amplified_values}")

            except modbus_tk.modbus.ModbusError as e:
                print(f"[ERROR] Failed to read from source server: {e}")

            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("\nAmplified server stopped by user.")

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

    finally:
        if 'amplified_server' in locals():
            amplified_server.stop()
            print("Amplified server stopped.")

if __name__ == "__main__":
    main()
