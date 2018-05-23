#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

######Config Section#####

###Color sensor
colorSensor = ColorSensor()
assert colorSensor.connected, "Connect a color sensor to any sensor port"
colorSensor.mode='COL-REFLECT'

###ultraSonic Sensor
sonicSensor = UltrasonicSensor() 
assert sonicSensor.connected, "Connect a single US sensor to any sensor port"
sonicSensor.mode='US-DIST-CM'

###ultraSonic sensor units in cm
sonicSensor.mode = 'US-DIST-CM'
units = sonicSensor.units

### Touch Sensor
touchSensor = TouchSensor()
assert touchSensor.connected, "Connect a touch sensor to any port" 

### Motors
rightMotor = LargeMotor('outB')
leftMotor = LargeMotor('outA')
hammerMotor = LargeMotor('outD')

speed = 500
forward = 360
back = -forward

##### Helper Funcions #####

def moveForward():
	rightMotor.run_to_rel_pos(position_sp=forward, speed_sp=speed, stop_action="hold")
	leftMotor.run_to_rel_pos(position_sp=forward, speed_sp=speed, stop_action="hold")

def haltWheels():
	rightMotor.stop()
	leftMotor.stop()

	#leftMotor.wait_while('running')
	#rightMotor.wait_while('running')

def getUnstuck():
	backupTime = 1000
	turnTime = 1500
	haltWheels()
	leftMotor.wait_while('running')
	rightMotor.wait_while('running')

	rightMotor.run_timed(time_sp=backupTime+turnTime, speed_sp=-speed)
	leftMotor.run_timed(time_sp=backupTime, speed_sp=-speed)
	
	rightMotor.wait_while('running')
	leftMotor.wait_while('running')

def isBlack():
	if(colorSensor.value() <= 3):
		return True
	else:
		return False

def checkSonic():
	return sonicSensor.value()/10 #convert mm to cm

def checkTouch():
	return touchSensor.value()

def collisionDetect():
	if(checkSonic() <= 10 or checkTouch()):
		return True
	else:
		return False

def smashThem():
	hammerMotor.run_to_rel_pos(position_sp=90, speed_sp=speed, stop_action="hold")
	hammerMotor.wait_while('running')
	hammerMotor.run_to_rel_pos(position_sp=-90, speed_sp=speed, stop_action="hold")
	hammerMotor.wait_while('running')

def protect():
	if(collisionDetect()): smashThem()

	
######## main #########
while True:
	while(not isBlack()):
		moveForward()
		if(collisionDetect()):
			getUnstuck()
	while(isBlack()):
		haltWheels()
		protect()
