import serial

def send_strings_via_uart(strings):
    # Initialize the serial connection
    port = 'COM3'  # Replace with your port
    baudrate = 38400  # Replace with your baudrate
    ser = serial.Serial(port, baudrate)
    
    for string in strings:
        # Add a newline character to indicate the end of the string
        data = string + '\n'
        # Send the string via UART
        ser.write(data.encode('utf-8'))
    
    # Close the serial connection
    print("All strings sent")
    ser.close()