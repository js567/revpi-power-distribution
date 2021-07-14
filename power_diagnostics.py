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
core3 = rpi.device.revpi01

# Socket setup for broadcasting UDP signal across local network

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Collection of LED signals for visual diagnostics communication

def flash_a1_green():
	
	time.sleep(0.01)
	core3.a1green.value = True
	core3.a1red.value = False	
	time.sleep(0.25)
	core3.a1green.value = False
	core3.a1red.value = False
	time.sleep(0.25)	

def flash_a1_a2_red_fast():

	time.sleep(0.001)
	core3.a1green.value = False
	core3.a1red.value = True	
	core3.a2green.value = False
	core3.a2red.value = False
	time.sleep(0.1)	
	core3.a1green.value = False
	core3.a1red.value = False	
	core3.a2green.value = False
	core3.a2red.value = True
	time.sleep(0.1)

def flash_a1_a2_red_slow():

	time.sleep(0.001)
	core3.a1green.value = False
	core3.a1red.value = True	
	core3.a2green.value = False
	core3.a2red.value = False
	time.sleep(0.6)	
	core3.a1green.value = False
	core3.a1red.value = False	
	core3.a2green.value = False
	core3.a2red.value = True
	time.sleep(0.6)

def cycle_fast():

	time.sleep(0.001)
	core3.a1green.value = False
	core3.a1red.value = True	
	core3.a2green.value = True
	core3.a2red.value = False
	time.sleep(0.1)	
	core3.a1green.value = True
	core3.a1red.value = False	
	core3.a2green.value = False
	core3.a2red.value = True
	time.sleep(0.1)

def cycle_slow():

	time.sleep(0.001)
	core3.a1green.value = False
	core3.a1red.value = True	
	core3.a2green.value = True
	core3.a2red.value = False
	time.sleep(0.6)	
	core3.a1green.value = True
	core3.a1red.value = False	
	core3.a2green.value = False
	core3.a2red.value = True
	time.sleep(0.6)

# Infinite loop to continuously broadcast UDP signal while power is on
# Eventually, a safe shutdown method should be implemented

while True: 

	try:		

		core3.a1green.value = True
		core3.a1red.value = False	
		core3.a2green.value = True
		core3.a2red.value = False

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

		# Bracketed voltage system to receive multiple inputs on same pin -- under construction
		
		rpi.io.InputStatus_1.value
		rpi.io.InputStatus_2.value
		rpi.io.InputStatus_3.value
		rpi.io.InputStatus_4.value

		print(message)
		print(core3.iocycle)
	
		sock.sendto(bytes(cur_time, "utf-8"), ("255.255.255.255", 30325))
		sock.sendto(bytes(str(digital_1), "utf-8"), ("255.255.255.255", 30326))
		sock.sendto(bytes(str(digital_2), "utf-8"), ("255.255.255.255", 30327))
		sock.sendto(bytes(str(analog_1), "utf-8"), ("255.255.255.255", 30328))
		sock.sendto(bytes(str(analog_2), "utf-8"), ("255.255.255.255", 30329))

		time.sleep(1 - 0.0015981)

	# On keyboard interrupt, flash LEDs red

	except KeyboardInterrupt:

		print(" UDP upload stopped")

		while True:
		
			flash_a1_a2_red_fast()
	

	
