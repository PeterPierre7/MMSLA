import serial
import numpy as np
from math import ceil
import json
import itertools

class MMSLA:
	def __init__(self, config_file, usb_path: str = "/dev/ttyS0"):

		# Get the config from file
		with open(config_file, 'r') as file:
			self.config = json.load(file)

		#  Create the Serial object to communicate
		self.__ser = serial.Serial(usb_path, 115200)
		# Set the default value for layer
		self.layer = 0
		# Load the layer height
		self.layer_height = self.config["layer_height"]
		# Load the parameter
		self.__update_next_layer()
		# Set the max buffer based on exposuretime 
		self.max_buffer = int(self.expo_time*0.1)
		# Set the bufffer variable
		self.buffer = list(itertools.repeat(0, self.max_buffer))
		# Set a default stepper_pos 
		self.stepper_pos = 0
		# Set a defualt value for layer based on stepper_pos 
		self.layer_from_stepper = 0

	def __update_next_layer(self):

		new_config = self.config["resine_changes"][0]

		self.resine_name = new_config["resine"]
		self.expo_time = new_config["exposure_time"]

		del self.config["resine_changes"][0]

		if len(self.config["resine_changes"]) > 0:
			self.next_layer_cut = self.config["resine_changes"][0]["layer"]
		else:
			self.next_layer_cut = -1

	def start(self):
		# Get the file to print path
		file_name = self.config["ctb_file"]
		# Ask the saturn to print the file
		self.__ser.write(f"M6030 '{file_name}'".encode())
		#  Ask the saturn to report every 10ms
		self.__ser.write("M156 S10".encode())
		# Ask for the stepper position
		self.__ser.write("M114".encode())

	def close(self):
		# Close the serial connection
		self.__ser.close()

	def __get_stepper_pos(self):
		# Ask for stepper position
		self.__ser.write("M114".encode())
		#  Read and decode
		msg = self.__ser.readline().decode()
		# print(msg)
		# The M114 status msg lenght is know
		expected_len = 51

		# If the msg is about stepper_pos
		if "Z:" in msg:
			# If the serial port is weird we flush TODO: better error handle
			while len(msg) != expected_len:
				# Flush the serial port
				self.__ser.flush()
				# Get clean msg
				msg = self.__ser.readline().decode()
				print(msg)
			# The msg is splited into each info
			splited_msg = msg.split()
			# The Z pos float is extracted
			self.stepper_pos = float(splited_msg[4][2:])
			print(f" Stepper pos : {self.stepper_pos}")
		# If the msg is not about stepper
		else:
			# Print the msg
			print(f"Saturn : {msg}")

	def __get_layer_from_stepper(self):
		# Update the stepper_pos
		self.__get_stepper_pos()
		# Update the buffer
		del self.buffer[0]
		self.buffer.append(self.stepper_pos)
		# Look at if the pos is stable
		print(f"STD : {np.std(self.buffer)}")
		if np.std(self.buffer) == 0.0:
			# If the position is stable
			# The layer is the stable position / by the std layer height
			self.layer_from_stepper = ceil(self.stepper_pos/ self.layer_height)
		# If not stable the layer stay the same
		print(f"Layer from stepper : {self.layer_from_stepper}")

	def switch_resine(self):
		print('resine_switched')

	def __update_layer(self):
		self.__get_layer_from_stepper()

	def print_loop(self):
		while True:
			if mmsla_print.__ser.in_waiting > 0:
				self.__update_layer()
				if self.layer == self.next_layer_cut:
					self.switch_resine()

# def increment_pos(tab: list, new_z: float, rolling_size: int = 50):

# 	tab.append(new_z)
# 	if len(tab) > rolling_size:
# 		del tab[0]


# def find_layer(z_pos: list, old: int, layer_height: float = 0.05) -> int:

# 	#  Define the constant for the export
# 	start = 0
# 	during = 1
# 	up = 2
# 	#  Calculate the history
# 	z_std = np.std(z_pos)
# 	#  If the history is stable
# 	if abs(z_std) < 0.00001:
# 		z_layer = z_pos[-1]
# 		#  The printer is at a specific layer
# 		layer = ceil(z_layer/layer_height)
# 		print(layer, z_layer)
# 		#  If the layer is different then it's the start of the layer
# 		if layer - old == 1:
# 			return [layer, start]
# 		# If the layer is the same then it's during the  layer
# 		elif layer - old == 0:
# 			return [layer, during]
# 		#  Else is not suppose to be possible
# 		else:
# 			print("odd layer history")
# 			return [layer, up]
# 	#  If the history is not constant, the printer is moving up and down
# 	else:
# 		print(f"up/down : mean :{z_std} z_pos:{z_layer}")
# 		return [old, up]


# def use_stepper_pos(self):
# 	#  Add the new position to the history
# 	increment_pos(tab=rolling_pos, new_z=stepper_pos)
# 	#  Find the layer based on the history
# 	layer_info = find_layer(z_pos=rolling_pos, old=old_layer)
# 	#  The layer from the Z position
# 	layer = layer_info[0]
# 	#  The start or middle of the layer
# 	adv = layer_info[1]
# 	#  Print the info
# 	print(f"Layer : {layer} - {adv}")

# 	if layer == layer_cut and adv == 2:
# 		__ser.write(" M25".encode())
# 		restart = input()
# 		__ser.write(restart.encode())

# 	return layer


# def read_json_file(path: str):
# 	# Read the data from the JSON file
# 	with open(path, "r") as f:
# 		file_config = json.load(f)
# 	return file_config


if __name__ == "__main__":

	# Create the MMSLA object
	mmsla_print = MMSLA("config/print_settings.json")
	#  Main loop
	mmsla_print.start()
	mmsla_print.print_loop()
	#  Close the serial connection
	mmsla_print.close()
