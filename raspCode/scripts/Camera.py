#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import picamera
from datetime import datetime
import os


videos_dir = '/home/pi/ros_catkin_ws/src/pei2020/VideoFiles/'
timestamp  =str(datetime.now())
os.mkdir(videos_dir + timestamp)
videos_dir = '/home/pi/ros_catkin_ws/src/pei2020/VideoFiles/' + timestamp + '/'
def talker():
    camera = picamera.PiCamera(resolution=(640, 480))
    while True:
        camera.start_recording(videos_dir + '1.h264')
        camera.wait_recording(30)
        for i in range(2, 500):
            camera.split_recording(videos_dir + '%d.h264' % i)
            camera.wait_recording(30)
        camera.stop_recording()



if __name__ == '__main__':
    try:
        talker()
    except:
        pass
