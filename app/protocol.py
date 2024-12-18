import serial
import serial.tools.list_ports


str_to_note = {
    "C4": 0, "C#4": 1, "D4": 2, "D#4": 3, "E4": 4, "F4": 5, "F#4": 6, "G4": 7, "G#4": 8, "A4": 9, "A#4": 10, "B4": 11,
    "C5": 12, "C#5": 13, "D5": 14, "D#5": 15, "E5": 16, "F5": 17, "F#5": 18, "G5": 19, "G#5": 20, "A5": 21, "A#5": 22, "B5": 23,
    "C6": 24, "C#6": 25, "D6": 26, "D#6": 27, "E6": 28, "F6": 29, "F#6": 30, "G6": 31, "G#6": 32, "A6": 33, "A#6": 34, "B6": 34,
}

SEQUENCE_END = 36

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
                str_data = string.strip()  # Remove extra whitespace
                if str_data not in str_to_note:
                    raise ValueError(f"Invalid note: {str_data}")
                note_index = str_to_note[str_data]

                # Send the note index as a single byte
                ser.write(bytes([note_index]))
                print(f"Sent: {str_data.strip()} as raw byte: {note_index}")
        ser.write(bytes([SEQUENCE_END]))

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
