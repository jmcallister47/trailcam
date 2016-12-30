#!/usr/bin/env python
'''Script that manages motion sensor, camera module and light
   When motion is detected, turn on infrared light, take and save picture, turn off light
   Maximum of one picture every 4 seconds'''
from gpiozero import MotionSensor
import subprocess
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO

def main():
    sensor = MotionSensor(4)
    writeToLogFile("STARTED NIGHT MODE AT " + str(datetime.now()))
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(5, GPIO.OUT) #setup light trigger
    while True:
        if sensor.motion_detected:
            turnOnLights()
            print "Lights on"
            sleep(1)
            takePicture() 
            print("Take picture")
            #sleep(3) 
            turnOffLights()
            print("Turn off lights")
            sleep(4) 
            writeToLogFile("Took one picture at " + str(datetime.now()))

'''Turns on IR Lights indefinetely'''
def turnOnLights():
    GPIO.output(5, 0)
    
'''Turns off all lights (IR and LED)'''
def turnOffLights():
    GPIO.output(5, 1)

'''Takes a picture and saves it with timestamp'''
def takePicture():
    now = datetime.now()
    timestamp = str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "-" + str(now.year) + "-" + \
                str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + ":" + str(now.second).zfill(2)
    filename = timestamp + "-night.jpg"
    subprocess.call(["sudo", "raspistill", "-o", "/home/pi/trailcam/tmp/" + filename]) 

def writeToLogFile(arg):
    file = open("/home/pi/trailcam/night/log.txt", "a");
    file.write(arg + "\n")
    file.close();

if __name__ == "__main__":
    main()
