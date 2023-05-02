import serial
import numpy as np
from math import ceil

def extract_z_pos(msg: str) -> float:

	if "Z:" in msg:
		splited_msg = msg.split()
		stepper_pos = float(splited_msg[4][2:])
		ser.write("M114".encode())
		return stepper_pos
		#print(f"Stepper position : {stepper_pos}")
	else:
		print(f"Saturn : {msg}")
		ser.write("M114".encode())
		return None

def increment_pos(tab:list, new_z:float, rolling_size:int=50):

	tab.append(new_z)
	if len(tab) > rolling_size:
		del tab[0]

def find_layer(z_pos:list, old:int, layer_height:float=0.05)-> int:

	#  Define the constant for the export
	start = 0
	during = 1
	up = 2
	#  Calculate the history
	z_mean = np.mean(z_pos)
	z_layer = z_pos[-1]
	#  If the history is stable 
	if abs(z_mean - z_pos[-1]) < 0.00001:
		#  The printer is at a specific layer
		layer = ceil(z_layer/layer_height)
		print(layer,z_layer )
		#  If the layer is different then it's the start of the layer
		if layer - old == 1:
			return [layer, start]
		# If the layer is the same then it's during the  layer
		elif layer - old == 0:
			return [layer, during]
		#  Else is not suppose to be possible
		else:
			print("odd layer history")
			return [layer ,up]
	#  If the history is not constant, the printer is moving up and down
	else:
		print(f"up/down : mean :{z_mean} z_pos:{z_layer}") 
		return [old, up]

def use_stepper_pos(stepper_pos:float,layer_cut:int, ser:serial.Serial):
	#  Add the new position to the history
		increment_pos(tab = rolling_pos, new_z = stepper_pos)
		#  Find the layer based on the history
		layer_info = find_layer(z_pos=rolling_pos, old=old_layer)
		#  The layer from the Z position
		layer = layer_info[0]
		#  The start or middle of the layer
		adv = layer_info[1]
		#  Print the info
		print(f"Layer : {layer} - {adv}")

		if layer == layer_cut and adv == 2:
				ser.write(" M25".encode())
				restart = input()
				ser.write(restart.encode())

		return layer



if __name__ == "__main__":
	#  Create the Serial object to communicate 
	ser = serial.Serial("/dev/ttyS0", 115200)
	#  Ask the saturn to report
	ser.write("M156 S10".encode())
	#  Define constant for layer logic
	rolling_pos = []
	old_layer = 1
	#  Define layer cut
	layer_cut = 6
	#  Main loop
	while True:
		#  If the printer give info
		if ser.in_waiting > 0:
			#  Read and decode
			msg = ser.readline().decode()
			#  Extract the Z stepper position
			stepper_pos = extract_z_pos(msg=msg)
			if stepper_pos is not None: #  If a new position
				#  Use the new stepper position
				old_layer = use_stepper_pos(stepper_pos=stepper_pos,layer_cut= layer_cut,ser= ser)
	#  Close the serial connection
	ser.close()

