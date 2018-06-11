# **************************************************
# SOURCES
# https://www.anavi.org/article/209/
# https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051
# **************************************************

# **************************************************
# IMPORT LIBRARIES
# **************************************************
# Required libraries: GPIO, time, sleep, signal, sys
# **************************************************

import RPi.GPIO as GPIO
import time
from time import sleep
import signal
import sys

# **************************************************
# PIN SETUP
# **************************************************
# Four GPIO pins are needed for the actuators, solenoids (both solenoids share the same relay so they only use one pin), and ultrasonic sensors
# **************************************************

GPIO.setmode(GPIO.BOARD)

ActuatorPin = 3
SolenoidPin = 5

x_pinTrigger = 13
x_pinEcho = 15

# **************************************************
# TURNING OFF PROCEDURE WHEN INTERRUPTED
# **************************************************
# Cleanup GPIO when ending procedure. Press CTRL + C to end procedure
# **************************************************

def off(signal, frame):
    print("\nTurning off system\n")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, off)

# **************************************************
# SOLENOID INSTRUCTIONS
# **************************************************
# Solenoids push for 3 seconds then retract
# **************************************************

def push():
    sleep(2)
    print "Pushing forward\n"
	GPIO.output(SolenoidPin, GPIO.HIGH)

    sleep(3)

    print "Pulling back\n"
	GPIO.output(SolenoidPin, GPIO.LOW)
    sleep(2)

# **************************************************
# ACTUATOR INSTRUCTIONS
# **************************************************
# Actuators hold down for the duration of the procedure
# **************************************************

def actuate():
    sleep(2)
    print "Holding down\n"
	GPIO.output(ActuatorPin, GPIO.HIGH)

    sleep(3)

    print "Letting go\n"
	GPIO.output(ActuatorPin, GPIO.LOW)
    sleep(2)

# **************************************************
# PUSH & ACTUATE
# **************************************************
# Push the solenoids and while on high, actuate the pistons
# **************************************************

def pushAndActuate():
    print "Pushing solenoids\n"
	GPIO.output(SolenoidPin, GPIO.HIGH)
    sleep(2)
    print "Actuating pistons\n"
	GPIO.output(ActuatorPin, GPIO.HIGH)
    sleep(10)
    print "Retracting solenoids\n"
	GPIO.output(SolenoidPin, GPIO.LOW)
    sleep(10)
    print "Retracting pistons\n"
	GPIO.output(ActuatorPin, GPIO.LOW)
    sleep(2)

# **************************************************
# X-AXIS SENSOR
# **************************************************
# Use ultrasonic sensor to measure distance from sensor to plate
# **************************************************

GPIO.setup(x_pinTrigger, GPIO.OUT)
GPIO.setup(x_pinEcho, GPIO.IN)

def x_distance():
    GPIO.output(x_pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(x_pinTrigger, False)

    x_startTime = time.time()
    x_stopTime = time.time()

    while 0 == GPIO.input(x_pinEcho):
        x_startTime = time.time()

    while 1 == GPIO.input(x_pinEcho):
        x_stopTime = time.time()

    x_TimeElapsed = x_stopTime - x_startTime
    x_distance = (x_TimeElapsed * 34300) / 2

    print ("X Distance: %.1f cm" % x_distance)

    return x_distance

# **************************************************
# PROCEDURE
# **************************************************
"""
PSEUDOCODE FOR PROCEDURE
    1. Run x y distance sensor loop
    2. Break loop when x < 5cm & y < 5cm
    3. Enter push procedure
    4. Run x y distance sensor
    5. Run loop again if x > 3cm & y > 3cm, push and check again
    6. If x y distance < 3cm end procedure
"""
# **************************************************

def run():
    # Put solenoids and actuators into off position
    print "Setting up"
    GPIO.setup(SolenoidPin,GPIO.OUT)
    GPIO.output(SolenoidPin, GPIO.LOW)

    GPIO.setup(ActuatorPin,GPIO.OUT)
    GPIO.output(ActuatorPin, GPIO.LOW)

    sleep(5)

    # Main operation loop
    while True:
        print "Procedure start\n"

        GPIO.output(SolenoidPin, GPIO.LOW)
        GPIO.output(ActuatorPin, GPIO.LOW)

        # Wait for plate to enter 6cm distance
        while (x_distance() > 6.0):
            print("Plate is not ready\n")
            sleep(1)

        # Push the plate and hold it down
        sleep(3)
        pushAndActuate()

        print "Procedure complete. Please remove the plate.\n"

        # Wait for the plate to be removed. If nothing is there after 10 seconds, then the item has been removed
        sleep(10)
        while (x_distance() < 6.0):
            print("Please remove the plate\n")
            sleep(10)

run()
