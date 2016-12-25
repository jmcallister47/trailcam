# Trailcam
### Motion camera written predominantly in Python with automated Dropbox upload
The code is divided into 5 parts:
* **controller**: Manages various scripts. Controls which motion mode (day or night) is is being run and starts the Dropbox upload. 
* **day**: Motion mode that uses 3rd party motion software (https://github.com/ccrisan/motionpie). Does not require motion sensor by comparing images to detect motion. Produces images and video.  
* **night**: Custom motion scripts that detect motion via sensor, turn on infrared lights and take/save picture to tmp
* **thirdparty**: Dropbox-Uploader (https://github.com/andreafabrizi/Dropbox-Uploader) and motion-pie scripts 
* **upload**: Contains files to upload motion and log files to Dropbox if network connection available and deletes tmp files
* **tmp**: local motion files to be uploaded
