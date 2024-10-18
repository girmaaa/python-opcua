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
<<<<<<< HEAD

=======
>>>>>>> 55dc139c2579bd24f038921e0491afa7d4c25dd1
