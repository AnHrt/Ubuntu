#!/usr/bin/env python 
import rospy 
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

class FollowLine():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.bridge_object = CvBridge() # create the cv_bridge object
        self.image_received = 0 #Flag to indicate that we have already received an image

        #~~~~~~~~~~~~~~~~~~~~~ PUBLISHER & SUBSCRIBERS ~~~~~~~~~~~~~~~~~~~~~
        self.img_pub = rospy.Publisher("imagen", Image, queue_size=1)
        self.pub_cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size = 1)
        self.image_sub = rospy.Subscriber("video_source/raw", Image, self.image_cb)
        self.vel = Twist()

    def cleanup(self):
        self.vel.linear.x = 0
        self.vel.angular.z = 0
        self.pub_cmd_vel.publish(self.vel)
        
#~~~~~~~~~~~~~~~~~~~~ MAIN PROGRAM ~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__": 
    rospy.init_node("cv_bridge", anonymous=True) 
    FollowLine()