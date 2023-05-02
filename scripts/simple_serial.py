import serial
import threading


def send_command():
    user = ""
    while "stop" not in user:

        user = input("chitu g code to send")
        ser.write(user.encode())


def serial_read(ser: serial.Serial):
    while True:
        ser.write("M156 S10".encode())
        msg = ser.readline().decode()
        print(msg)


ser = serial.Serial("/dev/ttyS0", 115200)


x = threading.Thread(target=send_command)
x.start()
y = threading.Thread(target=serial_read, args=ser)
y.start()
