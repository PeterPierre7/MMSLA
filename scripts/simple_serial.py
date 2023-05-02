import serial
import threading


def send_command():
    user = ""
    while "stop" not in user:

        user = input("chitu g code to send\n")
        ser.write(user.encode())


def serial_read(ser: serial.Serial):
    while True:
        if ser.in_waiting > 0:
            ser.write("M156 S10".encode())
            msg = ser.readline().decode()
            print(msg)


ser = serial.Serial("/dev/ttyS0", 115200)


y = threading.Thread(target=serial_read, args=ser)
y.start()
# x = threading.Thread(target=send_command)
# x.start()
