# Serial demo

`Receiver.py` and `Sender.py` are examples of a request-response communication
pattern, running over serial.

# To test

  1. Create a virtual serial-port using `socat`, or use a real serial port:

    socat PTY,raw,echo=0,link=uart0 PTY,raw,echo=0,link=uart1

  2. Start the receiver on one end of the serial port, and specify the baud rate:

    ./Receiver.py uart0 115200

  3. Run the sender on the other end of the serial port, specifying the same baud rate:

    ./Sender.py uart1 115200
