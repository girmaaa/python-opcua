import time
import csv
import can
from opcua import Server
from datetime import datetime

# Setup CAN bus
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

# Create OPC UA server instance
server = Server()
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
uri = "http://example.org"
idx = server.register_namespace(uri)

# Create sensor object and variables
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

# Open CSV file to log latencies
with open('server_latency_log.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Timestamp", "Operation", "Latency (ms)", "RPM", "Speed", "FuelLevel"])

    try:
        while True:
            # Time OPC UA update
            opc_start_time = time.time()

            # Simulate sensor data
            new_rpm = (rpm_var.get_value() + 10) % 256
            new_speed = (speed_var.get_value() + 5.0) % 256
            new_fuel = (fuel_var.get_value() + 1.0) % 256

            # Update OPC UA variables
            rpm_var.set_value(new_rpm)
            speed_var.set_value(new_speed)
            fuel_var.set_value(new_fuel)

            opc_end_time = time.time()
            opc_latency = (opc_end_time - opc_start_time) * 1000  # Convert to milliseconds

            # Log OPC UA latency
            timestamp = datetime.now().isoformat()
            csvwriter.writerow([timestamp, "OPC UA", opc_latency, new_rpm, new_speed, new_fuel])

            # Time CAN transmission
            can_start_time = time.time()

            # Send data via CAN bus
            can_message = can.Message(arbitration_id=0x123, data=[new_rpm, int(new_speed), int(new_fuel)], is_extended_id=False)
            bus.send(can_message)

            can_end_time = time.time()
            can_latency = (can_end_time - can_start_time) * 1000  # Convert to milliseconds

            # Log CAN latency
            timestamp = datetime.now().isoformat()
            csvwriter.writerow([timestamp, "CAN", can_latency, new_rpm, new_speed, new_fuel])

            # Print summary to console
            print(f"OPC UA Latency: {opc_latency:.2f} ms, CAN Latency: {can_latency:.2f} ms")
            time.sleep(1)  # 1-second interval

    finally:
        server.stop()
        print("OPC UA Server stopped")

