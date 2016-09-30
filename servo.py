# Script to run Servo with Angle Values instead of PWM Values on the Raspberry Pi
# Usage: servo.py [pwmPin] [angle|offset as a angle]
# Examples:
#  - Will set the servo on Pin 17 to a angle of 45: servo.py 17 45
#  - Will set the servo on Pin 17 to a angle of 55 if it was 45 before: servo.py 17 +10
#  - Will set the servo on Pin 17 to a angle of 55 if it was 45 before: servo.py 17 -10
# (c) GPL https://github.com/SebiPanther/servo

import RPi.GPIO as GPIO, time, sys, getopt, os

path = "/run/servo/" #Path where the current angle gets stored
filePrefix = "pin" #Prefix for the file where the angle gets stored. It will get followed by the pin number
pwmInterval = 50 #PWM Interval in Hz
minValue = 1.5 #Minimum Interval Ration - please check if this correspond to your servo
maxValue = 14.5 #Maximum Interval Ration - please check if this correspond to your servo
minAngle = 0 #Minimum Angle
maxAngle = 180 #Maximum Angle
defaultAngle = 90 #If there is no current Angle avadible for this pin and only a offset is given this is the default

pin = int(sys.argv[1])
pathpin = path + filePrefix + str(pin)
direction = sys.argv[2][0]

if direction == "+" or direction == "-":

    angle = defaultAngle

    if os.path.isfile(pathpin):
        file = open(pathpin, "r")
        angle = int(file.read())
        file.close()

    if direction == "+":
        angle += int(sys.argv[2][1:])
    else:
        angle -= int(sys.argv[2][1:])

else:

    angle = int(sys.argv[2])

if angle < minAngle:
    angle = minAngle

if angle > maxAngle:
    angle = maxAngle

rangeValue = maxValue - minValue
oneAngleValue = rangeValue / maxAngle
newValue = minValue + (oneAngleValue * angle)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, pwmInterval)
file = open(pathpin, "w")

try:
    p.start(newValue)
    time.sleep(0.5)

    if not os.path.exists(path):
        os.makedirs(path)

    file.write(str(angle))

    print "New position is a angle of %d." % angle
finally:
    p.stop()
    GPIO.cleanup()
    file.close()
