
import ReadSensor
from time import sleep  
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
DEBUG = 1

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
# set up the SPI interface pins
# Cleanup any old GPIO mapping
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

while True:
    try:
        Volt = ReadSensor.ReadVoltage(0,SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print 'Voltage :={}'.format(Volt)
	p = (Volt/3.3-0.08)/0.09*.145*27.6799
        print 'Pressure :={}'.format(p)

	sleep(1)
    
    except KeyboardInterrupt:
        GPIO.cleanup() 
        break
