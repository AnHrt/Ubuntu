#!/usr/bin/env python 
import rospy 
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

#This class will receive a ROS image and transform it to opencv format 
class CompetitionRobot():
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.bridge_object = CvBridge() # create the cv_bridge object
        self.image_received = 0 #Flag to indicate that we have already received an image

        #~~~~~~~~~~~~~~~~~~~~~ PUBLISHER & SUBSCRIBERS ~~~~~~~~~~~~~~~~~~~~~
        self.img_pub = rospy.Publisher("imagen", Image, queue_size=1)
        self.pub_cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size = 1)
        self.image_sub = rospy.Subscriber("video_source/raw", Image, self.image_cb)
        self.vel = Twist()

        r=0.05 #wheel radius [m] 
        L=0.19 #wheel separation [m] 
        self.wr=0.0
        self.wl=0.0
        xtarget=0.0
        ytarget=0.0
        pos_theta=0.0 
        pos_x=0.0
        pos_y=0.0 
        v=0.0
        w=0.0
        inv = 0
        band = 1
        
	    #self.vel.linear.x = 0.1
        #********** INIT NODE **********### 
        freq=10 
        rate = rospy.Rate(freq) #20Hz  
        Dt =1/float(freq) #Dt is the time between one calculation and the next one 
        while not rospy.is_shutdown():
            print("pase el while chavos")
            if self.image_received:
                print("estoy dentro del if kbrns")
                imagen = self.cv_image.copy()
                imagen = cv2.resize(self.cv_image,(450,300))
                hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

                min_green = np.array([60,150,100])
                max_green = np.array([73,255,255])

                min_red = np.array([0,128,100])
                max_red = np.array([4,255,255])

                min_red1 = np.array([174,128,100])
                max_red1 = np.array([180,255,225])


                mask_g = cv2.inRange(hsv, min_green, max_green)
                mask_r1 = cv2.inRange(hsv, min_red, max_red)	
                mask_r2 = cv2.inRange(hsv, min_red1, max_red1)	
                mask_r = mask_r1 + mask_r2
                
                ret, thresh1 = cv2.threshold(mask_r,200,255,cv2.THRESH_BINARY_INV) 
                ret, thresh2 = cv2.threshold(mask_g,200,255,cv2.THRESH_BINARY_INV) 
                    #We use the mask with the original image to get the colored post-processed image
                    #res_g = cv2.bitwise_and(imagen,imagen, mask= mask_g)
                    #res_r = cv2.bitwise_and(imagen,imagen, mask= mask_r)
                print("Llegue aqui")
                    #self.img_pub.publish(self.bridge_object.cv2_to_imgmsg(thresh1, "mono8"))
            #self.img_pub.publish(self.bridge_object.cv2_to_imgmsg(thresh2, "mono8"))
            #self.img_pub.publish(self.bridge_object.cv2_to_imgmsg(thresh3, "mono8"))

                params = cv2.SimpleBlobDetector_Params()
                params.filterByArea = False
                params.filterByCircularity = True
                params.minCircularity = 0.74
                params.filterByConvexity = False
                params.filterByInertia = False

                detector = cv2.SimpleBlobDetector_create(params)
                
                kp_g = detector.detect(thresh2)
                kp_r = detector.detect(thresh1)

                kernel = np.ones((5, 5), np.uint8)
                eroded_r = cv2.erode(thresh1, kernel)
                eroded_g = cv2.erode(thresh2, kernel)

                blank = np.zeros((1,1))
                im_w_kpr = cv2.drawKeypoints(thresh1, kp_r, blank, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
                im_w_kpg = cv2.drawKeypoints(thresh2, kp_g, blank, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
            
                for keypoints in kp_g:
                    if keypoints.size > 50:
                        kp_g = True

                for keypoints in kp_r:
                    if keypoints.size > 50:
                        kp_r = True

                v=r*(self.wr+self.wl)/2 
                w=r*(self.wr-self.wl)/L

                pos_x += v*Dt*np.cos(pos_theta)
                pos_y += v*Dt*np.sin(pos_theta)
                pos_theta += w*Dt

            if pos_theta > np.pi:
                pos_theta = pos_theta - 2*np.pi
            elif pos_theta < -np.pi:
                pos_theta = pos_theta + 2*np.pi
            # mayor que > menos que <

            e_theta = np.arctan2(ytarget, xtarget) - pos_theta
            ed = np.sqrt(pow(xtarget - pos_x, 2) + pow(ytarget - pos_y, 2))

            Kv = 0.21
            Kw = 0.12

            if self.vel.linear.x > 0.2: self.vel.linear.x = 0.2

            if abs(e_theta) >= 0.1:
                self.vel.angular.z = Kw * e_theta
            elif abs(ed) >= 0.1:
                self.vel.angular.z = 0.0
                self.vel.linear.x = Kv * ed

            else: 
                self.vel.angular.z = 0.0
                self.vel.linear.x = 0.0
                pos_x = 0
                pos_y = 0
                ed = 0
            if inv == 0:
                band += 1
            else:
                band -= 1
                
            if band == 0:
                xtarget = 0.1
                ytarget = 0.0
            elif band == 1:
                xtarget = -1.0
                ytarget = 0.0
            elif band == 2:
                xtarget = 1.0
                ytarget = 0.0
            elif band == 3:
                xtarget = 0.1
                ytarget = 0.0
            elif band == 4:
                xtarget = -1.0
                ytarget = 0.0
            elif band == 5:
                xtarget = 1.0
                ytarget = 0.0
                

                if kp_g == True:
                    inv = 1
                
                elif kp_r == True:
                    self.vel.linear.x = 0.0
                    self.vel.angular.z = 0.0
                    ed = 0
                    e_theta = 0.0
                #if kp_r == True:
                #	self.vel.linear.x = 0.0


                #self.img_pub.publish(self.bridge_object.cv2_to_imgmsg(im_w_kpg, "rgb8"))
                self.pub_cmd_vel.publish(self.vel)
                self.img_pub.publish(self.bridge_object.cv2_to_imgmsg(im_w_kpr, "bgr8"))

                self.image_received = 0

                print 'error angular: ', e_theta
                print 'error lineal: ', ed
                print '\n'
                print 'posicion en x:', pos_x
                print 'posicion en y:', pos_y
                print '\n'
            
            r.sleep() 
                #cv2.destroyAllWindows() 

    def image_cb(self, ros_image): 
        print("ando en el cb")
            ## This function receives a ROS image and transforms it into opencv format  
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
        
############################### MAIN PROGRAM ###################################
if __name__ == "__main__": 
    rospy.init_node("cv_bridge", anonymous=True) 
    CompetitionRobot() 
