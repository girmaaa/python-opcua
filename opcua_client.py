import time
from opcua import Client, ua

class SubHandler:
    """
    Subscription handler that will be called whenever data changes.
    """
    def datachange_notification(self, node, val, data):
        print(f"Data change detected: {node} - New Value: {val}")

# Connect to the server
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()
print("Connected to OPC UA Server")

try:
    # Access sensor object
    root = client.get_root_node()
    sensor = root.get_child(["0:Objects", "2:Sensor"])
    
    # Get references to variables (temperature, humidity, pressure)
    temp_var = sensor.get_child("2:Temperature")
    hum_var = sensor.get_child("2:Humidity")
    pressure_var = sensor.get_child("2:Pressure")

    # Create a subscription to receive real-time updates
    handler = SubHandler()
    sub = client.create_subscription(100, handler)
    handle_temp = sub.subscribe_data_change(temp_var)
    handle_hum = sub.subscribe_data_change(hum_var)
    handle_pressure = sub.subscribe_data_change(pressure_var)

    # Let the client run indefinitely to receive updates
    while True:
        time.sleep(1)  # Keep the client running

finally:
    client.disconnect()
    print("Disconnected from OPC UA Server")

