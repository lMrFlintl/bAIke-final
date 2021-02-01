import numpy as np
from datetime import datetime
import csv
import os
import impactDetection
import picamera
import picamera.array
import cv2
import  time 

camera = picamera.PiCamera()
camera.resolution = (384, 288) # 1024, 768
camera.start_preview()
frame_checker = 0   

for i in range(10):
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        image = stream.array
        #print(image.shape)
        #print('Frame analyzed')
        date = datetime.now()
        result = impactDetection.impactDetection(image)
        print(datetime.now() - date)
