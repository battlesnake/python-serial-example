'''
Wrapper around Serial library
'''

from serial import Serial

class Uart():

	def __init__(self, path, baud=115200, read_timeout=1):
		self.impl = Serial(port=path, baudrate=baud, exclusive=True)
		self.read_timeout = read_timeout
		self.impl.reset_input_buffer()
		self.impl.reset_output_buffer()

	def __enter__(self, *args):
		self.impl.__enter__()
		return self

	def __exit__(self, *args):
		self.impl.__exit__()

	''' Read data into buffer, return buffer '''
	def read(self):
		# Wait for data to be available
		self.impl.timeout = self.read_timeout
		self.impl.read(0)
		# Read as much data as is available in the buffer
		self.impl.timeout = 0
		return self.impl.read(self.impl.inWaiting())

	''' Write data from buffer '''
	def write(self, data):
		self.impl.write(data)
