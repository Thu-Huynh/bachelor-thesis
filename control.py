import RPi.GPIO as GPIO
import time
import serial
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(17,1)
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
while True:
	if GPIO.input(2) == False:
		GPIO.output(17,0)
		time.sleep(1)
		GPIO.output(17,1)
		time.sleep(1)
		
		port.write('AT'+'\r\n')
		time.sleep(0.1)
		
		port.write('ATE0'+'\r\n')
		time.sleep(0.1)

		port.write('AT+CMGF=1'+'\r\n')
		time.sleep(0.1)

		port.write('AT+CNMI=2,1,0,0,0'+'\r\n')
		time.sleep(0.1)

		port.write('AT+CMGS="01224976978"'+'\r\n')
		time.sleep(0.1)

		port.write('Raspberry Pi xin chao'+'\r\n')
		port.write("\x1A")
		time.sleep(10)
		port.write('ATD01224976978;'+'\r\n')		
		
		
		
		
		
		
