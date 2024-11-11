OPC UA & CAN Bus Latency Measurement

This project provides a benchmark for measuring latency in an OPC UA server-client architecture combined with CAN bus communication. It includes scripts for setting up an OPC UA server and client, sending data over CAN bus, and analyzing latencies. This documentation provides a complete overview of the project, its components, and instructions on how to run and analyze latency in your setup.

This project simulates an OPC UA server that collects data and communicates via a CAN bus with a client, with a primary goal of measuring the latency of data transmission and update times.

The main components of the project include:

OPC UA server and client: For collecting, updating, and sharing sensor data (RPM, Speed, Fuel Level).
CAN bus setup: Emulating data transfer between server and client for automotive or industrial use cases.
Latency logging and analysis: Logging timestamps and calculating latency for CAN and OPC UA operations.
System Requirements

Python: Ensure Python 3.6+ is installed.
Pip packages: python-can, freeopcua, pandas, matplotlib.
SocketCAN: Configure a virtual CAN bus for testing (vcan0).
CSV support: Used for logging data in CSV format.
Installation and Setup

1.Clone the repository:
code
git clone https://github.com/girmaaa/python-opcua.git
cd python-opcua
2.Install required packages:
pip install python-can freeopcua pandas matplotlib
3.Set up virtual CAN (if using virtual CAN for testing):
code
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
How to Run the Benchmark

To start the OPC UA server, client, and perform latency analysis, follow these steps:

1.Run the OPC UA Server:
code
python opcua_can_server_benchmark.py
2.Run the OPC UA Client:
code
python opcua_can_client_benchmark.py
3.Run Latency Analysis: Once the server and client have been running long enough to gather data, analyze the latency:
code
python latency_analysis.py
Explanation of Each Script

1. opcua_can_server_benchmark.py
This script sets up an OPC UA server that:

Initializes a CAN bus on vcan0.
Sets up an OPC UA endpoint at opc.tcp://localhost:4840/freeopcua/server/.
Defines variables for RPM, Speed, and FuelLevel.
Logs and measures the OPC UA and CAN latency for each variable update in milliseconds, saving results to server_latency_log.csv.
The server logs timestamps and values each time data is updated and transmitted over CAN.

2. opcua_can_client_benchmark.py
This script sets up an OPC UA client that:

Connects to the OPC UA server.
Initializes a CAN bus interface to receive data from the server.
Reads RPM, Speed, and Fuel Level data from CAN messages.
Updates these values on the OPC UA server and logs latency.
Logs both CAN and OPC UA latency in client_latency_log.csv.
3. latency_analysis.py
This script calculates and visualizes the latency for OPC UA and CAN communications by:

Loading server and client timestamp logs.
Calculating the latency (difference between timestamps).
Converting latency into milliseconds.
Plotting the latency trends over time for both OPC UA and CAN, providing insights into latency consistency and reliability.
Latency Analysis

The analysis script reads server_latency_log.csv and client_latency_log.csv to plot latency in milliseconds for each communication protocol. Each latency measurement includes:

OPC UA Latency: Time taken for the OPC UA server to update variables.
CAN Latency: Time taken for data to be sent over CAN bus.
The resulting graphs provide insights into the responsiveness of each communication channel.

Results Interpretation

OPC UA Latency: Ideally under 1 ms for each update, as OPC UA is often low-latency in local setups. Larger values might indicate processing delays or network issues.
CAN Latency: Should also be minimal, but values may vary depending on the CAN hardware and configuration.
By evaluating the plotted latencies, you can determine:

Whether the setup meets real-time performance needs.
If any bottlenecks are present in data transmission.
Project Design Choices

OPC UA Protocol: Selected for flexibility in industrial automation applications.
CAN Bus Simulation: Virtual CAN (vcan0) was chosen for local development, allowing testing without physical CAN hardware.
Milliseconds for Latency: Latency measurements are converted to milliseconds to highlight performance and responsiveness. Millisecond precision is standard in real-time applications.
CSV Logging: CSV was chosen for timestamp logging due to its simplicity and compatibility with analysis tools.
Additional Design Considerations
Each component is modular, so real CAN hardware could be introduced with minimal adjustments. Similarly, the code is extensible for additional sensor data or advanced latency analysis techniques.

Troubleshooting

Server or Client Not Connecting: Ensure the OPC UA server is running before starting the client.
High Latency Readings: Check for background processes that may impact CPU performance. If testing on a shared network, try switching to a direct connection.
CAN Bus Setup Issues: Ensure virtual CAN (vcan0) is correctly set up. Use ip link show to verify.



