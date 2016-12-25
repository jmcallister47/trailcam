#Kills daytime motion process if already running
sudo pkill -f motion-camera.py
sudo pkill -9 -f raspistill #needed in case motion-camera.py ended mid-picture
