#!/usr/bin/env python 
import rospy 
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray, gray2rgb
from skimage.util import random_noise
from scipy.ndimage import uniform_filter, median_filter, gaussian_filter
from scipy.ndimage import correlate, convolve, sobel
from scipy.io import loadmat
from skimage.feature import match_template, canny
from matplotlib.patches import Rectangle

class FollowLine():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.bridge_object = CvBridge() # create the cv_bridge object
        self.image_received = 0 #Flag to indicate that we have already received an image

        #~~~~~~~~~~~~~~~~~~~~~ PUBLISHER & SUBSCRIBERS ~~~~~~~~~~~~~~~~~~~~~
        self.img_pub = rospy.Publisher("imagen", Image, queue_size=1)
        #self.pub_cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size = 1)
        self.img_sub = rospy.Subscriber("video_source/raw", Image, self.image_cb)
        #self.vel = Twist()

        while not rospy.is_shutdown():

            if self.image_received:

                imagen = self.cv_image.copy()
                imagen = cv2.resize(self.cv_image,(450,300))
                f1, ax1 = plt.subplots(figsize=(10,10))
                ax1.imshow(imagen, cmap=plt.cm.gray), ax1.axis('off')
                plt.show()
                edge_I = canny(imagen)
                imshow_gray(edge_I, "Canny Edge Image")
             
             
    def imshow_gray(img, title, size=(20,20)): #
        plt.figure(figsize=size)
        plt.imshow(img, cmap=plt.cm.gray), plt.axis('off'), plt.title(title)
        plt.show()            
             
    def image_cb(self, ros_image): 
        if not self.image_received:
            try:
                print("received ROS image, I will convert it to opencv")
                # We select bgr8 because it is the OpenCV encoding by default
                self.cv_image = self.bridge_object.imgmsg_to_cv2(ros_image, desired_encoding="bgr8")
                #self.cv_image = self.bridge_object.imgmsg_to_cv2(ros_image, desired_encoding="rgb8")
                self.image_received = 1 #Turn the flag on
            except CvBridgeError as e:
                print(e)
         
    def cleanup(self):
        self.vel.linear.x = 0
        self.vel.angular.z = 0
        self.pub_cmd_vel.publish(self.vel)
        
#~~~~~~~~~~~~~~~~~~~~ MAIN PROGRAM ~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__": 
    rospy.init_node("cv_bridge", anonymous=True) 
    FollowLine()