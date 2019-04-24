#!/usr/bin/env python

from Uart import Uart
from SerialJson import Codec
from sys import argv
from time import time

messages = [
		{ "type": "Greeting", "text": "Hello world" },
		{ "type": "Bullplop", "text": "Another message" }
]

# Serial port parameters from command-line
serial_port = argv[1]
baud = int(argv[2])

codec = Codec()

with Uart(serial_port, baud) as uart:
	# Send each message and wait for acknowledgement
	for message in messages:
		# Send
		uart.write(codec.encode(message))
		# Receive response (wait 1 second before timing out)
		deadline = time() + 1
		reply = None
		while not reply and time() < deadline:
			reply = codec.decode(uart.read())
		if reply:
			print("Response: " + reply[0])
		else:
			print("No response received")
