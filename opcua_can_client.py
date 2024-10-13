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
    # Access the root node
    root = client.get_root_node()
    
    # Get the sensor object
    sensor = root.get_child(["0:Objects", "2:Sensor"])
    
    # Get references to variables (RPM, Speed, Fuel Level)
    rpm_var = sensor.get_child("2:RPM")
    speed_var = sensor.get_child("2:Speed")
    fuel_var = sensor.get_child("2:FuelLevel")

    # Create a subscription to receive real-time updates
    handler = SubHandler()
    sub = client.create_subscription(100, handler)  # Adjust the publishing interval as needed

    # Subscribe to data changes for RPM, Speed, and Fuel Level
    handle_rpm = sub.subscribe_data_change(rpm_var)
    handle_speed = sub.subscribe_data_change(speed_var)
    handle_fuel = sub.subscribe_data_change(fuel_var)

    # Let the client run indefinitely to receive updates
    while True:
        time.sleep(1)  # Keep the client running

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.disconnect()
    print("Disconnected from OPC UA Server")

