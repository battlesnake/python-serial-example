from Kiss import Kiss
from Json import Json
from Parity import Parity

class Codec():

	def __init__(self):
		self.json = Json()
		self.parity = Parity()
		self.kiss = Kiss()

	''' Encode object to byte array '''
	def encode(self, obj):
		return self.kiss.encode(self.parity.encode(self.json.encode(obj)))

	''' Decode byte array to array of zero or more objects '''
	def decode(self, data):
		return [self.json.decode(self.parity.decode(frame)) for frame in self.kiss.decode(data)]
