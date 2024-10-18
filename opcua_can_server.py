import time
from opcua import Server
from datetime import datetime

# Create a server instance
server = Server()

# Set endpoint
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

# Setup namespace
uri = "http://example.org"
idx = server.register_namespace(uri)

# Create a new object for the Sensor
sensor = server.nodes.objects.add_object(idx, "Sensor")

# Create variables for RPM, Speed, and Fuel Level
rpm_var = sensor.add_variable(idx, "RPM", 0)
speed_var = sensor.add_variable(idx, "Speed", 0.0)
fuel_var = sensor.add_variable(idx, "FuelLevel", 0.0)

# Set the variables to be writable by clients
rpm_var.set_writable()
speed_var.set_writable()
fuel_var.set_writable()

# Starting the server
server.start()
print("OPC UA Server started at {}".format(server.endpoint))

try:
    while True:
        # Simulate data updates
        new_rpm = rpm_var.get_value() + 10  # Increment RPM by 10
        new_speed = speed_var.get_value() + 5.0  # Increment Speed by 5.0
        new_fuel = fuel_var.get_value() + 1.0  # Increment Fuel Level by 1.0
        
        # Update variable values
        rpm_var.set_value(new_rpm)
        speed_var.set_value(new_speed)
        fuel_var.set_value(new_fuel)
        
        print(f"Updated RPM: {new_rpm}, Speed: {new_speed}, Fuel Level: {new_fuel}")
        
        time.sleep(1)  # Wait for 1 second before updating again

finally:
    server.stop()
    print("OPC UA Server stopped")

