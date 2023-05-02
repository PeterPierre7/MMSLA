import serial
ser = serial.Serial("/dev/ttyS0", 115200)
cmd = "G28"
ser.write(cmd.encode())
user = ""
while "stop" not in user:
	user = input()
	ser.write(user.encode())
	try:
		res = ser.readline().decode()
		print("Saturn :" , res)
	except Exception as e:
		print(e)
ser.close()
