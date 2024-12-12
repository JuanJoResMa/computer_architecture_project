import serial
import serial.tools.list_ports


def list_available_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def send_strings_via_uart(strings, port='COM3', baudrate=38400):
    """
    Sends a list of strings via UART.

    :param strings: List of strings to send.
    :param port: Serial port to use (e.g., 'COM3').
    :param baudrate: Baudrate for the serial connection.
    """
    try:
        # Verificar si el puerto está disponible
        available_ports = list_available_ports()
        if port not in available_ports:
            raise ValueError(f"The port {port} is not available.")

        # Initialize the serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud.")

        for string in strings:
            if string:
                # Add a newline character to indicate the end of the string
                data = string.strip() + '\n'
                ser.write(data.encode('utf-8'))
                # Quitamos los saltos de línea extra al imprimir
                print(f"Sent: {data.strip()}")

        print("All strings sent successfully.")
    except serial.SerialException as e:
        print(f"Error with serial communication: {e}")
    except ValueError as e:
        print(f"Port error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")
