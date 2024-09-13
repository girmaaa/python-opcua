from opcua import Client
import time

# Setup client
client = Client("opc.tcp://localhost:4840")
client.connect()

try:
    # Get the object
    myobj = client.get_node("ns=2;i=2")  # Adjust based on your server setup
    while True:
        # Read the variable value
        temperature = myobj.get_value()
        print("Current Temperature: {}".format(temperature))
        time.sleep(1)
finally:
    client.disconnect()
    print("Client disconnected")

