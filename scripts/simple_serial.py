import serial
import threading


def send_command(ser: serial.Serial, stop_event: threading.Event):
    # If the event is not raised
    while not stop_event.is_set():
        # The user is ask a command
        user = input("Enter Chitu G code to send or type 'stop' to exit:\n")
        # If the user stop
        if user == 'stop':
            #The stop event is raised
            stop_event.set()
        else:
            # Else the command is send to the elegoo
            ser.write(user.encode())


def serial_read(ser: serial.Serial, stop_event: threading.Event):
    # If the event is not raised
    while not stop_event.is_set():
        # If the serial port is not empty
        if ser.in_waiting > 0:
            # Read the message
            msg = ser.readline().decode()
			# And print
            print(msg)

if __name__ == "__main__":
    # Create a serial connection with the elegoo
    ser = serial.Serial("/dev/ttyS0", 115200)
    # Ask the elegoo to report every 1 s
    ser.write("M156 S1000".encode())
    # Define a commun event for threading
    stop_event = threading.Event()
    # Define the first thread with the serial read function
    t1 = threading.Thread(target=serial_read, args=(ser, stop_event))
    # Start reading the serial port
    t1.start()
    # Define the second thread with the send command function
    t2 = threading.Thread(target=send_command, args=(ser, stop_event))
    # Start of the user to print function
    t2.start()
    # If close, wait for both of them then close the serial connection
    t2.join()
    t1.join()

    ser.close()
