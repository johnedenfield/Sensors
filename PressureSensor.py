#!/usr/bin/python2.7

from time import sleep  
from datetime import datetime
from twython import Twython

import RPi.GPIO as GPIO
import sqlite3, os, ReadSensor

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
GPIO.setwarnings(False)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Setup Database
def LogPressure(conn,pressure):
	# Log Pressure to database
	# Get Time
	d=datetime.now();
	dstr=d.strftime('%m/%d/%y %H:%M:%S');

	c = conn.cursor();
	c.execute('INSERT INTO PressureSensor VALUES (?, ?)' , (dstr,pressure));

	conn.commit();
	conn.close();


def ConnToDb():
	# Conect to database
	DIR ='/var/www/Flask/App/db'
	FILE ='SensorData.db'
	fname = os.path.join(DIR,FILE)
	conn = sqlite3.connect(fname);
	return conn

def PostOnTwitter(notify):
	CONSUMER_KEY = 'Nig203jWvBYfE35ZV9LRPAi6b'
	CONSUMER_SECRET = 'l94snn65kWq0TZExZb24hstDsjDAsq5rpxXAvGJEidCdDdlbNO'
	ACCESS_KEY = '27339700-MsNEfeSlTu9UNiY2TEkb1aTRZdOpxoEbi83xOI8Dc'
	ACCESS_SECRET = 'mmQx58Ilp9ngP6Lm48yS2nChvSDxH4vz58LJi4DPKOBD7'
	
	api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 
	api.update_status(status=notify)
	

# Start Logging
conn =ConnToDb();
c = conn.cursor();
c.execute( ''' CREATE TABLE IF NOT EXISTS PressureSensor (DateAndTime text , Pressure real) ''');

conn.commit();
conn.close();




Volt = ReadSensor.ReadVoltage(0,SPICLK, SPIMOSI, SPIMISO, SPICS)
pressure= (Volt/3.3-0.08)/0.09*.145*27.6799 #Inches WC
			
conn=ConnToDb();
LogPressure(conn,pressure)

if pressure < 2.0:
	
	PostOnTwitter('Water the Christmas tree: Current water level is {:.2f} Inches'.format(pressure))
		

	


