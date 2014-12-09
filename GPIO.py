#!/usr/bin/python2.7

import RPi.GPIO as GPIO 
from time import sleep
import os

GPIO.setmode(GPIO.BCM)


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
ACRelay = 4
 
# set up the interface
GPIO.setup(ACRelay, GPIO.OUT)
HSdir='/var/www/Flask/App/GPIO'
fname = os.path.join(HSdir,'GPIOHandShake.txt')
LogFile ='GPIOStatusLog.txt';
PrevInput='NA'

while True:
	try:
        # Try to open the file        
		with open(fname, 'r') as f:
			Input = f.read();
		
		
		IO=int(Input.split()[0])
        # Print request 
		
		if Input != PrevInput:
			with open(LogFile,'a') as f:
				f.write(Input)
				
			if IO == ACRelay: 
			# If IO command is the AC Relay
				if 'ON' in Input: #ON
					GPIO.output(ACRelay,GPIO.LOW)
	     
				if "OFF" in Input: #OFF
					GPIO.output(ACRelay,GPIO.HIGH)
        
		PrevInput=Input;
		        
		sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup() 
		break

	except:
		pass
        