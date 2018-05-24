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
    print("\nTurning off ultrasonic distance sensors...\n Alignment complete...")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, off)

# **************************************************
# SOLENOID INSTRUCTIONS
# **************************************************
# Solenoids push for 3 seconds then retract
# **************************************************

def push():
    print "pushing forward"
	GPIO.output(SolenoidPin, GPIO.HIGH)

    sleep(3)

    print "pulling back"
	GPIO.output(SolenoidPin, GPIO.LOW)

# **************************************************
# ACTUATOR INSTRUCTIONS
# **************************************************
# Actuators hold down for the duration of the procedure
# **************************************************

def actuate():
    print "holding down"
	GPIO.output(ActuatorPin, GPIO.HIGH)

    sleep(3)

    print "letting go"
	GPIO.output(ActuatorPin, GPIO.LOW)

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
    print "Setting up"
    GPIO.setup(SolenoidPin,GPIO.OUT)
    GPIO.output(SolenoidPin, GPIO.LOW)

    GPIO.setup(ActuatorPin,GPIO.OUT)
    GPIO.output(ActuatorPin, GPIO.LOW)

    sleep(2)

    while True:
        print "Procedure start"

        while (x_distance() > 6.0):
            print("\nPlate is not ready")
            sleep(1)

        push()
        sleep(1)

        while (x_distance() > 4.0):
            print("\nPlate is not aligned... Enter push procedure again")
            sleep(1)
            push()

        print "\nSUCCESS..."
        print ("Final X Distance: %.1f cm" % x_distance())
        print "Ending alignment procedure\n"

        sleep(1)

        print "\nStarting \n"
        actuate()

run()
