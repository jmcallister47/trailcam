#!/usr/bin/env python
'''Checks if there is an internet connection and if there is:
      1. Creates directory in Dropbox with current date as name
      2. Uploads all local files in  ~/trailcam/tmp to Dropbox directory
      3. If the files were uploaded properly, deletes all local copies
      4. Uploads controller and upload log files
   If no internet connection, do nothing 
   Should be done at reboot and every 4 hours as cronjob (see example of crontab in home directory) '''
import subprocess
import urllib2
from datetime import datetime
import os
import sys

def main():
    uploadedSuccesfully = False 
    if isInternetConnection():
        uploadLogFiles() #useful for debugging in case of large amount of motion files
        numberOfFiles = upload() #attempts to upload files 
        if isInternetConnection(): #if network conection at beginning and end of upload, files uploaded without error
            deleteLocalFiles()
            writeToLogFile("SUCCESS: Uploaded " + str(numberOfFiles) + " at " + str(datetime.now()))
            uploadLogFiles() #upload log files again with new information
    else:
        writeToLogFile("FAILED: No network connection at " + str(datetime.now()))

def isInternetConnection():
    try:
        urllib2.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

'''Creates Dropbox directory and uploads all files in /trailcam/tmp to Dropbox
   Returns number of files uploaded'''
def upload():
    now = datetime.now()
    directory = str(now.month) + "-" + str(now.day) + "-" + str(now.year) + "-uploaded"
    cmd = "/home/pi/trailcam/thirdparty/Dropbox-Uploader/dropbox_uploader.sh mkdir /" + directory #make new directory
    with open(os.devnull, 'w') as fp:
        p = subprocess.Popen(cmd, shell = True, stdout = fp)
        p.communicate()
    files = [f for f in os.listdir("/home/pi/trailcam/tmp")]
    numberOfFiles = 0
    for file in files:
        numberOfFiles += 1
        cmd = "/home/pi/trailcam/thirdparty/Dropbox-Uploader/dropbox_uploader.sh upload -s " + \
              "/home/pi/trailcam/tmp/" + str(file) + " /" + directory  
        with open(os.devnull, 'w') as fp:
            p = subprocess.Popen(cmd, shell = True, stdout = fp)
            p.communicate() #wait for file to upload
    return numberOfFiles

def deleteLocalFiles():
    cmd = "sudo rm /home/pi/trailcam/tmp/*"
    with open(os.devnull, 'w') as fp:
        p = subprocess.Popen(cmd, shell = True, stdout = fp)
        p.communicate()

def writeToLogFile(arg):
    file = open("/home/pi/trailcam/upload/log.txt", "a");
    file.write(arg + "\n")
    file.close();

def uploadLogFiles():
    cmd = "/home/pi/trailcam/thirdparty/Dropbox-Uploader/dropbox_uploader.sh upload  " + \
          "/home/pi/trailcam/controller/log.txt /LOG_FILES/controller-log.txt"     
    #upload controller log    
    with open(os.devnull, 'w') as fp:
        p = subprocess.Popen(cmd, shell = True, stdout = fp)
    cmd = "/home/pi/trailcam/thirdparty/Dropbox-Uploader/dropbox_uploader.sh upload  " + \
          "/home/pi/trailcam/upload/log.txt /LOG_FILES/upload-log.txt"
    #upload upload log
    with open(os.devnull, 'w') as fp:
        p = subprocess.Popen(cmd, shell = True, stdout = fp)
    #upload night log
    cmd = "/home/pi/trailcam/thirdparty/Dropbox-Uploader/dropbox_uploader.sh upload  " + \
          "/home/pi/trailcam/night/log.txt /LOG_FILES/night-log.txt"
    with open(os.devnull, 'w') as fp:
        p = subprocess.Popen(cmd, shell = True, stdout = fp)
    #upload day log
    cmd = "/home/pi/trailcam/thirdparty/Dropbox-Uploader/dropbox_uploader.sh upload " + \ 
          "/home/pi/trailcam/day/log.txt /LOG_FILES/day-log.txt"
    with open(os.devnull, 'w') as fp:
        p = subprocess.Popen(cmd, shell = True, stdout = fp)

if __name__ == "__main__":
    main()
