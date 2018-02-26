# **************************************************
# SOURCES
# https://www.anavi.org/article/209/
# https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051
# **************************************************

# **************************************************
# IMPORT LIBRARIES 
# **************************************************

import RPi.GPIO as GPIO
import time
from time import sleep
import signal 
import sys

# **************************************************
# PIN SETUP 
# **************************************************

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 11
Motor2B = 13
Motor2E = 15

x_pinTrigger = 33
x_pinEcho = 37

y_pinTrigger = 32
y_pinEcho = 36

# **************************************************
# TURNING OFF PROCEDURE WHEN INTERRUPTED
# **************************************************

def off(signal, frame):
    print("\nTurning off ultrasonic distance sensors...\n Alignment complete...")
    GPIO.cleanup()
    sys.exit(0)
    
signal.signal(signal.SIGINT, off)
    
# **************************************************
# SOLENOID INSTRUCTIONS
# **************************************************

def push():
    print "Ready to push"
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)

    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)

    print "Going forwards"
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

    sleep(1)

    print "Going backwards"
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

    sleep(1)

    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    print "Push complete"

# **************************************************
# X-AXIS SENSOR
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
# Y-AXIS SENSOR
# **************************************************

GPIO.setup(y_pinTrigger, GPIO.OUT)
GPIO.setup(y_pinEcho, GPIO.IN)

def y_distance():
    GPIO.output(y_pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(y_pinTrigger, False)
    
    y_startTime = time.time()
    y_stopTime = time.time()
    
    while 0 == GPIO.input(y_pinEcho):
        y_startTime = time.time()
    
    while 1 == GPIO.input(y_pinEcho):
        y_stopTime = time.time()
        
    y_TimeElapsed = y_stopTime - y_startTime
    y_distance = (y_TimeElapsed * 34300) / 2
     
    print ("Y Distance: %.1f cm" % y_distance)
    
    return y_distance

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

def run():
    print "Setting up"
    sleep(3)

    print "Procedure start"

    while (x_distance() > 8.0 or y_distance() > 8.0):
        print("\nPlate is not ready")
        sleep(1)
        
    push()

    while (x_distance() > 5.0 or y_distance() > 5.0):
        print("\nPlate is not aligned... Enter push procedure again")
        sleep(1)
        push()

    print "\nSUCCESS..."
    print ("Final X Distance: %.1f cm" % x_distance())
    print ("Final Y Distance: %.1f cm" % y_distance())
    print "Ending alignment procedure\n"
        
    GPIO.cleanup()

run()