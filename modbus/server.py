#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modbus TCP server responding with simulated sensor values:
- Water level in tank (%)
- Chlorine residual (mg/L ×100)
- Valve pressure (psi)
"""

import time
import random
import modbus_tk
import modbus_tk.defines as defines
from modbus_tk import modbus_tcp

def main():
    """Modbus TCP Server."""
    try:
        # Create the server
        server = modbus_tcp.TcpServer(address='0.0.0.0', port=502)

        # Start the server
        print("Starting Modbus-tk server...")
        server.start()

        # Add slave ID 1
        slave_1 = server.add_slave(1)

        # Create 3 holding registers starting from address 0
        slave_1.add_block('0', defines.HOLDING_REGISTERS, 0, 3)

        print("Server is running. Listening on port 502.")
        print("Serving the following simulated values:")
        print("- Water tank level (%): 60–70")
        print("- Chlorine residual (mg/L ×100): 1000–1500")
        print("- Valve pressure (psi): 20–40")

        while True:
            # Generate random values
            water_level_percent = random.randint(60, 70)
            chlorine_residual = random.randint(1000, 1500)  # Represented as mg/L * 100
            valve_pressure = random.randint(30, 50)

            # Set all three values in the register block
            slave_1.set_values('0', 0, [water_level_percent, chlorine_residual, valve_pressure])

            # Print to console for debugging
            #print(f"Water Level: {water_level_percent}%, "
            #      f"Chlorine: {chlorine_residual / 100:.2f} mg/L, "
            #      f"Valve Pressure: {valve_pressure} psi")

            time.sleep(2)

    except modbus_tk.modbus.ModbusError as exc:
        print(f"Modbus error: {exc}")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
    finally:
        if 'server' in locals():
            server.stop()
            print("Server stopped.")

if __name__ == "__main__":
    main()
