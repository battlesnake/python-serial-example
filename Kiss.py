''' Minimal KISS/SLIP framing/deframing '''

'''
KISS/SLIP protocol, provides packet interface over character interface

Commonly used by some amateur TNCs, and also to encapsulate IP packets over
serial links
'''

from collections import deque
from itertools import islice

# Singleton representing end of frame, emitted by KissDecoder
end_of_frame = object()

# Singleton representing that the current frame is invalid and has been
# terminated, emitted by KissDecoder
invalid_frame = object()

class KissConfig(object):
	''' Default KISS configuration '''
	FEND = 0xc0
	FESC = 0xdb
	TFEND = 0xdc
	TFESC = 0xdd

class Kiss():

	def __init__(self, config=KissConfig()):
		self.config = config
		self.encoder = _KissByteEncoder(config=config)
		self.decoder = _KissByteDecoder(config=config)
		self.rxbuf = deque()

	''' Encode frame to a byte array '''
	def encode(self, frame):
		if frame is None:
			return None
		data = bytearray()
		data += self.encoder.open()
		for byte in frame:
			data += self.encoder.encode(byte)
		data += self.encoder.close()
		return data

	''' Decode a byte array to zero or more frames '''
	def decode(self, data):
		if data is None:
			return []
		decoded = []
		for item in data:
			if isinstance(item, int):
				# Byte
				decoded.append(self.decoder.decode(item))
			elif isinstance(item, (bytes, bytearray)):
				# Bytes/ByteArray
				for byte in item:
					decoded.append(self.decoder.decode(byte))
			else:
				raise TypeError('Invalid parameter type (expect byte/bytes/bytearray)')
		self.rxbuf += [byte for byte in decoded if byte is not None]
		# For convenience
		buffered = self.rxbuf
		# Extract frames
		begin = 0
		it = 0
		end = len(buffered)
		out = []
		while it < end:
			sym = buffered[it]
			it = it + 1
			if sym == invalid_frame:
				begin = it
			elif sym == end_of_frame:
				out.append(bytes(list(islice(buffered, begin, it-1))))
				begin = it
		# Remove processed data from buffer
		for i in range(0, begin):
			self.rxbuf.popleft()
		# How to return multiple frames at once?
		return out


class _KissByteEncoder(object):
	''' Encodes one byte at a time, returns bytes '''

	def __init__(self, config=KissConfig()):
		self.config = config
		self.is_open = False

	def open(self):
		if self.is_open:
			raise AssertionError('Frame is already open')
		self.is_open = True
		return bytes([self.config.FEND])

	def close(self):
		if not self.is_open:
			raise AssertionError('Frame is not open')
		self.is_open = False
		return bytes([self.config.FEND])

	def idle(self):
		return bytes([self.config.FEND])

	def encode(self, data):
		''' Encodes a byte of data '''
		if not isinstance(data, int):
			raise TypeError('Invalid parameter type (expected byte)')
		if data == self.config.FEND:
			return bytes([self.config.FESC, self.config.TFEND])
		elif data == self.config.FESC:
			return bytes([self.config.FESC, self.config.TFESC])
		else:
			return bytes([data])

class _KissByteDecoder():
	''' Decodes one byte at a time, returns bytes/None/end_of_frame/invalid_frame '''

	def __init__(self, config=KissConfig):
		self.config = config
		self.previous_char = None
		self.is_open = False

	#pylint: disable=too-many-branches
	def decode(self, byte):
		''' Returns byte or invalid_frame / end_of_frame or None '''
		if not isinstance(byte, int):
			raise TypeError('Invalid parameter type (expected byte)')
		''' Result placeholder '''
		result = None

		if self.previous_char == self.config.FEND:
			if byte == self.config.FEND:
				# Multiple FENDs, do nothing
				pass
			else:
				# Previous byte was FEND, this one isn't - open frame
				self.is_open = True

		if self.is_open:
			# A frame is open, parse the byte as data
			if byte == self.config.FEND:
				if self.previous_char == self.config.FESC:
					# FEND after FESC, invalid
					self.is_open = False
					result = invalid_frame
				else:
					# Close the frame
					self.is_open = False
					result = end_of_frame
			elif self.previous_char == self.config.FESC:
				# Escaped byte
				if byte == self.config.TFESC:
					result = self.config.FESC
				elif byte == self.config.TFEND:
					result = self.config.FEND
				else:
					# Invalid escape sequence
					self.is_open = False
					result = invalid_frame
			elif byte == self.config.FESC:
				# Nothing
				pass
			else:
				# Verbatim
				result = byte
		# Update decoder state
		self.previous_char = byte
		# Return decoded data
		return result
