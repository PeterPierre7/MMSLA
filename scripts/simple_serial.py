import serial
import threading


def send_command(ser, stop_event):
    while not stop_event.is_set():
        user = input("Enter Chitu G code to send or type 'stop' to exit:\n")
        ser.write(user.encode())
        if user == 'stop':
            stop_event.set()


def serial_read(ser, stop_event):
    while not stop_event.is_set():
        if ser.in_waiting > 0:
            ser.write("M156 S10".encode())
            msg = ser.readline().decode()
            print(msg)
        if stop_event.is_set():
            break


ser = serial.Serial("/dev/ttyS0", 115200)
stop_event = threading.Event()

t1 = threading.Thread(target=serial_read, args=(ser, stop_event))
t1.start()

t2 = threading.Thread(target=send_command, args=(ser, stop_event))
t2.start()

t2.join()
t1.join()

ser.close()
