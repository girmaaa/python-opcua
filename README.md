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
   
