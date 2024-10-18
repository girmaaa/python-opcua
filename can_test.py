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
