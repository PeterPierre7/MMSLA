import serial
import threading

def send_command():
	user = input("chitu g code to send")
	ser.write(user.encode())

ser = serial.Serial("/dev/ttyS0", 115200)
ser.write("M156 S10".encode())

x = threading.Thread(target=send_command)

user = ""
x.start()
while "stop" not in user:
	try:
		res = ser.readline().decode()
		print("Saturn :" , res)
	except Exception as e:
		print(e)
ser.close()
