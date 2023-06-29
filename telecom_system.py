import serial
import serial.tools.list_ports
import time

# Specify the device name to search for
device_name = 'Silicon Labs CP210x USB to UART Bridge'

# Find the port number for the device
ports = serial.tools.list_ports.comports()
port_number = None
for port in ports:
    if device_name in port.description:
        port_number = port.device
        break

if port_number is None:
    print(f"Device '{device_name}' not found.")
    exit()

# Configure the serial connection
baud_rate = 57600  # Adjust to match your telemetry module's baud rate

# Open the serial connection
ser = serial.Serial(port_number, baud_rate)

# Wait for user input to start sending data
while True:
    s = input("Enter start code: ")
    if s == "start":
        break

# Send and receive data
while True:
    data_to_send = b'fire'
    #ser.write(data_to_send)
    ser.writelines(data_to_send)
    print("Data sent:", data_to_send)
    time.sleep(1)

    #received_data = ser.readline()
    #print("Received data:", received_data.decode())

# Close the serial connection
ser.close()
