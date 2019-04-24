'''
Reed-Solomon error-correcting code
'''

import reedsolo

class Parity():

	def __init__(self):
		self.codec = reedsolo.RSCodec()

	''' Add parity to a packet '''
	def encode(self, packet):
		if packet is None:
			return None
		return self.codec.encode(packet)

	''' Strip parity from a packet and correct error, return None if uncorrectable '''
	def decode(self, packet):
		if packet is None:
			return None
		try:
			return self.codec.decode(packet)
		except reedsolo.ReedSolomonError:
			return None
