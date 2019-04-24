#!/usr/bin/env python

from Uart import Uart
from SerialJson import Codec
from sys import argv

serial_port = argv[1]
baud = int(argv[2])

codec = Codec()

with Uart(serial_port, baud) as uart:
	# Loop endlessly
	while True:
		# Receive messages
		messages = codec.decode(uart.read())
		# Print and acknowledge messages
		for message in messages:
			# Print
			print(message["type"] + ": " + message["text"])
			# Send ack
			uart.write(codec.encode("OK"))
