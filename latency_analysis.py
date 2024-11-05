import pandas as pd
import matplotlib.pyplot as plt

# Load CSV files
server_data = pd.read_csv("server_timestamps.csv")
client_data = pd.read_csv("client_timestamps.csv")

# Parse timestamps to datetime format for calculations
server_data['Timestamp'] = pd.to_datetime(server_data['Timestamp'])
client_data['Timestamp'] = pd.to_datetime(client_data['Timestamp'])

# Separate OPC UA and CAN data for server and client
opcua_server_data = server_data[server_data['Protocol'] == 'OPC UA'].reset_index(drop=True)
opcua_client_data = client_data[client_data['Protocol'] == 'OPC UA'].reset_index(drop=True)
can_server_data = server_data[server_data['Protocol'] == 'CAN'].reset_index(drop=True)
can_client_data = client_data[client_data['Protocol'] == 'CAN'].reset_index(drop=True)

# Ensure we have matching records; if necessary, truncate to smallest length
min_length_opcua = min(len(opcua_server_data), len(opcua_client_data))
min_length_can = min(len(can_server_data), len(can_client_data))

opcua_server_data = opcua_server_data.iloc[:min_length_opcua]
opcua_client_data = opcua_client_data.iloc[:min_length_opcua]
can_server_data = can_server_data.iloc[:min_length_can]
can_client_data = can_client_data.iloc[:min_length_can]

# Calculate latency in milliseconds by subtracting server timestamp from client timestamp and converting to milliseconds
opcua_latency_ms = (opcua_client_data['Timestamp'] - opcua_server_data['Timestamp']).dt.total_seconds() * 1000
can_latency_ms = (can_client_data['Timestamp'] - can_server_data['Timestamp']).dt.total_seconds() * 1000

# Plot the latency for each protocol in milliseconds
plt.figure(figsize=(10, 6))
plt.plot(opcua_latency_ms, label="OPC UA Latency (ms)")
plt.plot(can_latency_ms, label="CAN Latency (ms)")
plt.xlabel("Sample Number")
plt.ylabel("Latency (ms)")
plt.title("OPC UA vs CAN Bus Latency (in ms)")
plt.legend()
plt.show()

