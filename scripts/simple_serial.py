import serial
import threading

def send_command(ser):
    while True:
        user = input("Enter Chitu G code to send or type 'stop' to exit:\n")
        if "stop" in user:
            break
        ser.write(user.encode())


def serial_read(ser):
    while True:
        if ser.in_waiting > 0:
            ser.write("M156 S10".encode())
            msg = ser.readline().decode()
            print(msg)


ser = serial.Serial("/dev/ttyS0", 115200)

t1 = threading.Thread(target=serial_read, args=(ser,))
t1.start()

t2 = threading.Thread(target=send_command, args=(ser,))
t2.start()
