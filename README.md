# Trailcam
Motion camera written predominantly in Python with automated Dropbox upload
The code is divided into 5 parts:
    1. **controller**: Manages various scripts. Controls which motion mode (day or night) is is being run and starts the Dropbox upload. 
    2. **day**: Motion mode that uses 3rd party motion software (https://github.com/ccrisan/motionpie). Does not require motion sensor by comparing images to detect motion. Produces images and video.  
    3. **night**: Custom motion scripts that detects motion via sensor, turns on infrared lights and takes a picture
    4. **thirdparty**: Dropbox-Uploader(https://github.com/andreafabrizi/Dropbox-Uploader) and motion-pie scripts 
    5. **upload**: Contains files to upload motion and log files to Dropbox if network connection available and deletes /tmp files
    6. **tmp**: local motion files to be uploaded
