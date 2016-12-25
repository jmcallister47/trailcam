#!/usr/bin/env python
'''Script that manages motion sensor, camera module and light
   When motion is detected, turn on infrared light, take and save picture, turn off light
   Maximum of one picture every 5 seconds'''
from gpiozero import MotionSensor
import subprocess
from datetime import datetime
from time import sleep

def main():
    sensor = MotionSensor(4)
    writeToLogFile("STARTED NIGHT MODE AT " + str(datetime.now()))
    while True:
        if sensor.motion_detected:
            turnOnLights()
            sleep(1) #wait one second to ensure lights are all on
            takePicture() 
            sleep(2) 
            turnOffLights()
            sleep(3) 
            writeToLogFile("Took one picture at " + str(datetime.now()))

'''Turns on IR Lights indefinetely'''     
def turnOnLights():
    subprocess.call(["sudo", "i2cset", "-y", "1", "0x70", "0x00", "0xa5"]) #turn on IR lights    
    subprocess.call(["sudo", "i2cset", "-y", "1", "0x70", "0x09", "0x0f"]) #turn gain to full
    subprocess.call(["sudo", "i2cset", "-y", "1", "0x70", "0x01", "0x32"]) #full brightness
    subprocess.call(["sudo", "i2cset", "-y", "1", "0x70", "0x03", "0x32"])
    subprocess.call(["sudo", "i2cset", "-y", "1", "0x70", "0x06", "0x32"])
    subprocess.call(["sudo", "i2cset", "-y", "1", "0x70", "0x08", "0x32"]) 

'''Turns off all lights (IR and LED)'''
def turnOffLights():
    subprocess.call(["sudo", "i2cset", "-y", "1", "0x70", "0x00", "0x00"])

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
