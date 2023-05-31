import serial
import serial.tools.list_ports
# pip install pyserial

# Specify the device name to search for
device_name = 'CP2102 USB to UART Bridge Controller'

# Find the port number for the device
ports = serial.tools.list_ports.comports()
port_number = None
print("Hi")
print(serial.tools.list_ports.grep(1).send(b'HI'))
for port in ports:
    if device_name in port.description:
        port_number = port.device
        break

if port_number is None:
    print(f"Device '{device_name}' not found.")
    exit()

# Configure the serial connection
baud_rate = 9600  # Adjust to match your telemetry module's baud rate

# Open the serial connection
ser = serial.Serial(port_number, baud_rate)

# Send and receive data as before
data_to_send = b'Hello, World!'
ser.write(data_to_send)
received_data = ser.read(10)
print(received_data)

# Close the serial connection
ser.close()
