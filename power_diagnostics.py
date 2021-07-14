'''
Author: Jack Stevenson
Date: 7/9/2021
Purpose: Receives inputs from power distribution modules on RevPi AIO module and 
         broadcast UDP signal containing diagnostics information to server.
	 This program is intended to be running from the startup of the RevPi until
	 it looses power or is shut down safely. 
'''

import revpimodio2
import socket
import datetime
import time
import tkinter

# IO object to interact to give and receive signals

rpi = revpimodio2.RevPiModIO(autorefresh=True)

# Socket setup for broadcasting UDP signal across local network

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Infinite loop to continuously broadcast UDP signal while power is on
# Eventually, a safe shutdown method should be implemented

while True: 

	try:

		# Get current time to timestamp UDP message 
	
		cur_time = datetime.datetime.now().isoformat()
	
		# Input reading for each pin
	
		digital_1 = rpi.io.InputValue_1.value
		digital_2 = rpi.io.InputValue_2.value
		analog_1 = rpi.io.InputValue_3.value
		analog_2 = rpi.io.InputValue_4.value
	
		if digital_1 == -1:
			digital_1 = 0

		if analog_1 == -1:
			analog_1 = 0

		message = cur_time+' '+str(digital_1)+' '+str(digital_2)+' '+str(analog_1)+' '+str(analog_2)

		# Bracketed voltage system to receive multiple inputs on same pin
	
		#if digital_1 
		
		rpi.io.InputStatus_1.value
		rpi.io.InputStatus_2.value
		rpi.io.InputStatus_3.value
		rpi.io.InputStatus_4.value

		print(message)
	
		sock.sendto(bytes(cur_time, "utf-8"), ("255.255.255.255", 30325))
		sock.sendto(bytes(str(digital_1), "utf-8"), ("255.255.255.255", 30326))
		sock.sendto(bytes(str(digital_2), "utf-8"), ("255.255.255.255", 30327))
		sock.sendto(bytes(str(analog_1), "utf-8"), ("255.255.255.255", 30328))
		sock.sendto(bytes(str(analog_2), "utf-8"), ("255.255.255.255", 30329))

		time.sleep(1 - 0.0015981)

	except KeyboardInterrupt:
		
		print(" UDP upload stopped")
		break

	

	
