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
		# Set a default stepper_pos 
		self.stepper_pos = 0
		# Set a defualt value for layer based on stepper_pos 
		self.layer_from_stepper = 0

	def __update_buffer(self):
		# Set the max buffer based on exposuretime 
		self.max_buffer = int(self.expo_time*0.1)
		# Set the bufffer variable
		self.buffer = list(itertools.repeat(self.layer, self.max_buffer))

	def __update_next_layer(self):

		new_config = self.config["resine_changes"][0]

		self.resine_name = new_config["resine"]
		self.expo_time = new_config["exposure_time"]

		del self.config["resine_changes"][0]

		if len(self.config["resine_changes"]) > 0:
			self.next_layer_cut = self.config["resine_changes"][0]["layer"]
		else:
			self.next_layer_cut = -1

		# Once the infos are loaded, a buffer is created based on expose
		self.__update_buffer()

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
		if "Z:" in msg and len(msg) == expected_len:
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
		if np.std(self.buffer) < 0.001:
			# If the position is stable
			# The layer is the stable position / by the std layer height
			self.layer_from_stepper = ceil(self.stepper_pos/ self.layer_height)
		# If not stable the layer stay the same
		print(f"Layer from stepper : {self.layer_from_stepper}")

	def switch_resine(self):
		print('resine_switched')
		self.__update_next_layer()
		print(f"New resine : {self.resine_name}")


	def __update_layer(self):
		self.__get_layer_from_stepper()
		if self.layer_from_stepper == self.layer+1:
			self.layer = self.layer_from_stepper
		print(f"Usable layer : {self.layer}")

	def print_loop(self):
		while True:
			if mmsla_print.__ser.in_waiting > 0:
				self.__update_layer()

				if self.layer == self.next_layer_cut:
					self.switch_resine()

if __name__ == "__main__":

	# Create the MMSLA object
	mmsla_print = MMSLA("config/print_settings.json")
	#  Main loop
	mmsla_print.start()
	mmsla_print.print_loop()
	#  Close the serial connection
	mmsla_print.close()
