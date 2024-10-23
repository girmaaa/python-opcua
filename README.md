# python-opcua
# OPC UA Client-Server Integration with CAN Bus

## Project Overview

This project involves the integration of an OPC UA (Open Platform Communications Unified Architecture) client with a CAN (Controller Area Network) bus system. The primary goal is to facilitate real-time data exchange between an OPC UA server and a CAN bus, enabling seamless communication and data monitoring.

## Technologies Used

- **Python**: The primary programming language used for developing both the OPC UA client and server.
- **opcua**: A Python library for implementing OPC UA clients and servers.
- **python-can**: A Python library for interfacing with CAN networks.
- **SocketCAN**: A set of open-source CAN drivers and a networking stack in the Linux kernel.
- **Git**: Version control system used for tracking changes in the codebase and collaboration.

## Project Structure

- **Server**: The server-side code is responsible for providing data through OPC UA. It is implemented and successfully pushed to the repository.
- **Client**: The client-side code subscribes to the OPC UA server for real-time data updates and integrates with the CAN bus to receive and process CAN messages.

## Features

- **Data Subscription**: The OPC UA client subscribes to specific data points (RPM, Speed, Fuel Level) from the OPC UA server. It utilizes a subscription handler to receive and process data change notifications.
- **CAN Bus Communication**: The client continuously listens for CAN messages and prints them to the console, allowing for real-time monitoring and interaction with the CAN network.
- **Error Handling**: The client code includes exception handling to manage errors that may arise during OPC UA connection or data processing.

## Implementation Steps

1. **Setup the OPC UA Server**: 
   - Implemented and tested the OPC UA server to expose data points that the client would subscribe to.
  
2. **Develop the OPC UA Client**:
   - Established a connection to the OPC UA server using the `opcua` library.
   - Subscribed to data changes for key metrics (RPM, Speed, Fuel Level) from the server.
   - Implemented a subscription handler to handle incoming data changes.
  
3. **Integrate CAN Bus**:
   - Configured the CAN bus using the `python-can` library.
   - Implemented functionality to receive and print CAN messages in real time.
  
4. **Merge Conflicts and Version Control**:
   - Managed code changes using Git, resolving merge conflicts as necessary during collaboration.
   - Pushed the final version of both client and server code to the GitHub repository.

     detail description about the code

     1. Python CAN Bus Code (Sending and Receiving CAN Messages)
This is a simple script that demonstrates sending and receiving CAN messages using Python and the python-can library.
code;-
import can

# Connect to the virtual CAN interface
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Sending a CAN message
message = can.Message(arbitration_id=0x123, data=[0x11, 0x22, 0x33, 0x44], is_extended_id=False)
bus.send(message)
print(f"Message sent on {bus.channel_info}")

# Receiving a CAN message
message = bus.recv(10.0)  # Timeout in 10 seconds
if message:
    print(f"Message received: {message}")
else:
    print("No message received")

    What it does:

Connecting to the CAN bus: The script connects to a virtual CAN interface (vcan0) using the socketcan backend.
Sending a CAN message: It creates a CAN message with a specific arbitration ID (0x123) and a data payload ([0x11, 0x22, 0x33, 0x44]). This message is sent on the bus.
Receiving a CAN message: The script then waits for up to 10 seconds (recv(10.0)) to receive any CAN message. If a message is received, it prints it; otherwise, it prints "No message received."

2. Python Client Code for CAN Bus and OPC UA Integration
This script integrates both the CAN bus and OPC UA protocol from the client-side. It subscribes to OPC UA data changes and receives CAN messages.

code:-

import time
import can
from opcua import Client, ua

class SubHandler:
    """Subscription handler that will be called whenever data changes."""
    def datachange_notification(self, node, val, data):
        print(f"OPC UA Data change: {node} - New Value: {val}")

# Connect to the OPC UA server
opcua_client = Client("opc.tcp://localhost:4840/freeopcua/server/")
opcua_client.connect()
print("Connected to OPC UA Server")

# Setup CAN bus
can_bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

try:
    # Subscribe to OPC UA data changes
    handler = SubHandler()
    sub = opcua_client.create_subscription(100, handler)  # 100ms publishing interval
    sub.subscribe_data_change(rpm_var)
    sub.subscribe_data_change(speed_var)
    sub.subscribe_data_change(fuel_var)

    while True:
        # Receive CAN data (wait for 10 seconds max for a message)
        can_message = can_bus.recv(10.0)
        if can_message:
            print(f"CAN Bus Message: {can_message}")

        time.sleep(1)  # Keep client running

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    opcua_client.disconnect()
    print("Disconnected from OPC UA Server")

    What it does:

Connects to the OPC UA server: The client connects to the OPC UA server using the specified endpoint (opc.tcp://localhost:4840/freeopcua/server/).
Sets up the CAN bus: The client also connects to the virtual CAN bus interface (vcan0) using the python-can library.
Subscribes to OPC UA data changes: A subscription is created to monitor changes in the RPM, Speed, and Fuel Level variables from the OPC UA server. The SubHandler class is responsible for printing the updated values whenever any of these variables change.
Receives CAN data: The script continuously listens for CAN messages. If a CAN message is received within the 10-second timeout, it prints the message.
Error handling and cleanup: If an error occurs during the script's execution, it prints the error and ensures that the OPC UA client disconnects cleanly.


3. Server-Side OPC UA and CAN Bus Integration
This code is responsible for acting as the OPC UA server and integrates with the CAN bus by sending sensor data through both OPC UA and CAN.

code:-

import time
import can
from opcua import Server

# Setup CAN bus
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

# Create OPC UA server instance
server = Server()
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
uri = "http://example.org"
idx = server.register_namespace(uri)

# Create sensor object
sensor = server.nodes.objects.add_object(idx, "Sensor")
rpm_var = sensor.add_variable(idx, "RPM", 0)
speed_var = sensor.add_variable(idx, "Speed", 0.0)
fuel_var = sensor.add_variable(idx, "FuelLevel", 0.0)

# Set the variables to be writable by clients
rpm_var.set_writable()
speed_var.set_writable()
fuel_var.set_writable()

# Start OPC UA server
server.start()
print("OPC UA Server started")

try:
    while True:
        # Simulate sensor data
        new_rpm = rpm_var.get_value() + 10
        new_speed = speed_var.get_value() + 5.0
        new_fuel = fuel_var.get_value() + 1.0

        # Ensure values are within the valid byte range (0-255)
        rpm_byte = int(new_rpm) % 256
        speed_byte = int(new_speed) % 256
        fuel_byte = int(new_fuel) % 256

        # Update OPC UA variables
        rpm_var.set_value(new_rpm)
        speed_var.set_value(new_speed)
        fuel_var.set_value(new_fuel)

        # Send data via CAN bus
        can_message = can.Message(arbitration_id=0x123, data=[rpm_byte, speed_byte, fuel_byte], is_extended_id=False)
        bus.send(can_message)
        print(f"CAN message sent: RPM={rpm_byte}, Speed={speed_byte}, Fuel={fuel_byte}")

        time.sleep(1)  # 1-second interval

finally:
    server.stop()
    print("OPC UA Server stopped")

What it does:

Creates an OPC UA server: This code sets up an OPC UA server with an endpoint at opc.tcp://localhost:4840/freeopcua/server/.
Creates sensor variables: The script adds three sensor variables (RPM, Speed, and Fuel Level) to the OPC UA server, which are writable by clients.
Simulates sensor data: It continuously simulates changes in RPM, Speed, and Fuel Level, updating the OPC UA variables with these new values.
Sends CAN messages: The script also sends this sensor data over the CAN bus using a CAN message with an arbitration ID of 0x123.

4. Client-Side Python Code for CAN Bus Integration (CAN-only)
This script focuses on connecting to the CAN bus from the client-side and receiving messages from it.

code:-
import can

# Connect to the virtual CAN interface
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Sending a CAN message
message = can.Message(arbitration_id=0x123, data=[0x11, 0x22, 0x33, 0x44], is_extended_id=False)
bus.send(message)
print(f"Message sent on {bus.channel_info}")

# Receiving a CAN message
message = bus.recv(10.0)  # Timeout in 10 seconds
if message:
    print(f"Message received: {message}")
else:
    print("No message received")

    What it does:

Connects to the virtual CAN interface: The script connects to the vcan0 CAN interface.
Sends a CAN message: It sends a basic CAN message with a specific arbitration ID (0x123) and some example data ([0x11, 0x22, 0x33, 0x44]).
Receives a CAN message: It waits for a message on the CAN bus for up to 10 seconds. If a message is received, it prints it.




## Conclusion

This project successfully demonstrates the integration of OPC UA communication with a CAN bus system. The OPC UA client can effectively subscribe to real-time data updates from the server while concurrently processing CAN messages. This setup lays the groundwork for further enhancements, such as data logging and analysis or additional protocols.

## Future Work

- Explore additional features, such as data logging or visualization tools.
- Expand the functionality to support more data points and enhance the client-server communication.
- Investigate security measures for OPC UA communications and CAN bus integrations.

## Getting Started
2.Install required libraries:
pip install opcua python-can
3.Start the OPC UA server (already implemented).
4.Run the OPC UA client.
   
