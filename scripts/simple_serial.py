import serial
import threading

def send_command():
	while "stop" not in user:
		user = input("chitu g code to send")
		ser.write(user.encode())

def serial_read(ser: serial.Serial):
	while True:
		msg = ser.readline().decode()
		print(msg)

ser = serial.Serial("/dev/ttyS0", 115200)
ser.write("M156 S10".encode())


x = threading.Thread(target=send_command)
x.start()
y = threading.Thread(target=send_command, args=ser)
y.start()


