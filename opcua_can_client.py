import time
import can
from opcua import Client

class SubHandler:
    def datachange_notification(self, node, val, data):
        print(f"OPC UA Data change: {node} - New Value: {val}")

# Connect to OPC UA server
opcua_client = Client("opc.tcp://localhost:4840/freeopcua/server/")
opcua_client.connect()
print("Connected to OPC UA Server")

# Setup CAN bus
can_bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

try:
    # Subscribe to OPC UA data changes
    root = opcua_client.get_root_node()
    sensor = root.get_child(["0:Objects", "2:Sensor"])
    rpm_var = sensor.get_child("2:RPM")
    speed_var = sensor.get_child("2:Speed")
    fuel_var = sensor.get_child("2:FuelLevel")

    handler = SubHandler()
    sub = opcua_client.create_subscription(100, handler)
    sub.subscribe_data_change(rpm_var)
    sub.subscribe_data_change(speed_var)
    sub.subscribe_data_change(fuel_var)

    while True:
        # Receive CAN data
        can_message = can_bus.recv(10.0)
        if can_message:
            print(f"CAN Bus Message: {can_message}")
        
        time.sleep(1)  # Keep client running

finally:
    opcua_client.disconnect()
    print("Disconnected from OPC UA Server")
