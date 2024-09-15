import time
import random
from opcua import ua, Server
from datetime import datetime

# Create an instance of the OPC UA Server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# Setup server namespaces and objects
uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)
objects = server.get_objects_node()

# Create a new object called 'Sensor'
sensor = objects.add_object(idx, "Sensor")

# Add variables (simulated real-time data) for temperature, humidity, and pressure
temp_var = sensor.add_variable(idx, "Temperature", 0.0)
hum_var = sensor.add_variable(idx, "Humidity", 0.0)
pressure_var = sensor.add_variable(idx, "Pressure", 0.0)

# Allow write access to variables (optional)
temp_var.set_writable()
hum_var.set_writable()
pressure_var.set_writable()

# Start the server
server.start()
print("OPC UA Server started at opc.tcp://0.0.0.0:4840/freeopcua/server/")

try:
    while True:
        # Simulate real-time sensor data updates
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(30.0, 50.0), 2)
        pressure = round(random.uniform(950, 1050), 2)

        # Update variables with new values
        temp_var.set_value(temperature)
        hum_var.set_value(humidity)
        pressure_var.set_value(pressure)

        print(f"Updated sensor data at {datetime.now()}:")
        print(f"Temperature: {temperature} °C, Humidity: {humidity} %, Pressure: {pressure} hPa")
        time.sleep(2)  # Update every 2 seconds to simulate real-time data

finally:
    # Stop the server when done
    server.stop()
