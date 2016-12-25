#!/usr/bin/env python
'''Determines what time of day it is, and begins the day or night motion detection mode
   Sleeps until mode needs to be switched (control day/night times with constants below)
   Uploads all motion and log files when first run and immediately before a mode switch
   This script is intended to be run as a cron job @reboot or run with a /etc/init.d script'''
import datetime
from subprocess import Popen
from os import devnull
from time import sleep

MORNING_TIME = 6 #constants that represent day and night mode in hours
NIGHT_TIME = 18 #day from 6AM to 6PM

def main():
    writeToLogFile("Starting motion-controller script at " + str(datetime.datetime.now()))
    sleep(60) #wait for one minute to allow network connection to be established upon boot
    runExecutable("/home/pi/trailcam/upload/upload.py") #attempts to upload files
    while(True):
        writeToLogFile("Killing all motion scripts at " + str(datetime.datetime.now()))
        cmd = "/home/pi/trailcam/controller/kill-motion.sh" #end all motion scripts to release camera
        with open(devnull, 'w') as fp:
            p = Popen(cmd, shell = True, stdout = fp)
            p.communicate() #pauses until all motion is killed
        if isDay() == True:
            runExecutable("/home/pi/trailcam/day/motion-start.sh") #start day motion
            writeToLogFile("Running day-time motion at " + str(datetime.datetime.now()))
            sleepUntil(NIGHT_TIME)
        else:
            runExecutable("/home/pi/trailcam/night/motion-start.sh") #start night motion
            writeToLogFile("Running night-time motion at " + str(datetime.datetime.now()))
            sleepUntil(MORNING_TIME)
        writeToLogFile("Attempting to upload at " + str(datetime.datetime.now()))
        runExecutable("/home/pi/trailcam/upload/upload.py") #attempts to upload files every time mode is switched

'''Return a boolean, True if day and false if night based on constants above'''
def isDay():
    now = datetime.datetime.now()
    return now.hour >= MORNING_TIME and now.hour < NIGHT_TIME

'''Runs a script given the scripts location as a string
   Fire and forget execution: will not wait for script to be completed
   Precondition: file must be executable
   Ex. runExecutable("/home/pi/someScript.sh")'''
def runExecutable(fileLocation):
    FNULL = open(devnull, 'w') #equivalent of DEVNULL for python 3.0+
    Popen(fileLocation, shell=True, stdout=FNULL, stderr=FNULL) #runs script and hides output

def writeToLogFile(arg):
    file = open("/home/pi/trailcam/controller/log.txt", "a");
    file.write(arg + "\n")
    file.close();

'''Pauses until specified hour in one minute increments'''
def sleepUntil(wakeHour):
    currentHour = datetime.datetime.now().hour
    while(currentHour != wakeHour):
        sleep(60) #sleep for 1 minute
        currentHour = datetime.datetime.now().hour

if __name__ == "__main__":
    main()

