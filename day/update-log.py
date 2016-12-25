#! /usr/bin/env python
'''Updates log.txt with date and event captured message
   Script is automatically executed whenever a motion event is recorded by daytime motion'''
from datetime import datetime

def main():
    writeToLogFile("Motion event at " + str(datetime.now()))

def writeToLogFile(arg):
    file = open("/home/pi/trailcam/day/log.txt", "a");
    file.write(arg + "\n")
    file.close();

if __name__ == "__main__":
    main()
