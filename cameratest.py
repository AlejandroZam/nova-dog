from picamera2 import Picamera2
from time import sleep

camera = Picamera2()

camera.start_preview()
sleep(5)
camera.start_and_capture_file('/home/dog/Desktop/nova-dog/cameratest_1.png')
