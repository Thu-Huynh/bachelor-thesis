import RPi.GPIO as GPIO
import time
import os

sensor = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.OUT)

while True:
	current_state = GPIO.input(sensor)
	if current_state == 1:
		 GPIO.output(20,0)
		
	else:
		GPIO.output(20,1)
		
