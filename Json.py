'''
JSON serialiser and deserialiser consumers
'''

import json

class Json():

	def __init__(self, encoding='utf-8'):
		self.encoding = encoding

	''' Encode an object as a JSON packet '''
	def encode(self, packet):
		if packet is None:
			return None
		if self.encoding is None:
			return json.dumps(packet)
		else:
			return json.dumps(packet).encode(self.encoding)

	''' Decodea an object from a JSON packet '''
	def decode(self, packet):
		if packet is None:
			return None
		if isinstance(packet, (bytes, bytearray)):
			if self.encoding is None:
				raise AssertionError('Encoding has not been specified')
			else:
				return json.loads(packet.decode(self.encoding))
		elif isinstance(data, str):
			return json.loads(data)
