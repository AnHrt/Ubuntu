from djitellopy import Tello
import cv2
#from cv2 import VideoCapture
import numpy as np

def empty(x):
	pass

def main():

	Width = 640
	Height = 480
	tolerance = 100

	Param1 = 100
	Param2 = 30
	MinRadius = 10
	MaxRadius = 40

	takeoff_counter=0
	move = 0

	"""drone = Tello()
	drone.connect()
	drone.battery()

	drone.streamoff()
	drone.streamon()"""
	capture = cv2.VideoCapture(0)
	cv2.namedWindow("Parameters")
	cv2.resizeWindow("Parameters",640,240)
	cv2.createTrackbar("MinRadius","Parameters",1,255,empty)
	cv2.createTrackbar("MaxRadius","Parameters",1,255,empty)
	cv2.createTrackbar("Param1","Parameters",10,200,empty)
	cv2.createTrackbar("Param2","Parameters",1,100,empty)

	cv2.setTrackbarPos("MinRadius","Parameters",MinRadius)
	cv2.setTrackbarPos("MaxRadius","Parameters",MaxRadius)
	cv2.setTrackbarPos("Param1","Parameters",Param1)
	cv2.setTrackbarPos("Param2","Parameters",Param2)

	while True:

		#frame_read = drone.get_frame_read().frame
		ret, frame = capture.read()
		img = cv2.resize(frame,(Width,Height))
		
		MinRadius = cv2.getTrackbarPos("MinRadius","Parameters")
		MaxRadius = cv2.getTrackbarPos("MaxRadius","Parameters")
		Param1 = cv2.getTrackbarPos("Param1","Parameters")
		Param2 = cv2.getTrackbarPos("Param2","Parameters")

		imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		imgGray = cv2.medianBlur(imgGray, 5)
		rows = imgGray.shape[0]

		circles = cv2.HoughCircles(imgGray,cv2.HOUGH_GRADIENT,1,rows/8, param1 = Param1, param2 = Param2, minRadius = MinRadius, maxRadius = MaxRadius)

		if circles is not None:
			circles = np.uint16(np.around(circles))
			for i in circles[0, :]:
				cx = i[0]
				cy = i[1]
				center = (cx, cy)
				# circle center
				cv2.circle(img, center, 1, (0, 100, 100), 3)
				# circle outline
				radius = i[2]
				cv2.circle(img, center, radius, (255, 0, 255), 3)
				#obtaining directions
				"""if (cx<(Width/2)-tolerance):
					#left
					move=1
				elif (cx>(Width/2)+tolerance):
					#right
					move=2
				else:
					move=0
		else:
			move=0

		if (takeoff_counter==0):
			#drone.takeoff()
			takeoff_counter=1
		if (move==0):
			lr_speed=0
			fb_speed=0
			ud_speed=0
			yaw_speed=0
			print("Stop")

		if (move==1):
			lr_speed=-50
			fb_speed=0
			ud_speed=0
			yaw_speed=0
			print("Left")

		if (move==2):
			lr_speed=50
			fb_speed=0
			ud_speed=0
			yaw_speed=0
			print("Right")
		
		#drone.send_rc_control(lr_speed,fb_speed,ud_speed,yaw_speed)"""

		cv2.imshow("Imagen original",img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			#drone.streamoff()
			#drone.land()
			break
	# cap.release()
	cv2.destroyAllWindows()

try:
    main()
    
except KeyboardInterrupt:
	print ('KeyboardInterrupt exception is caught')
	#drone.streamoff()
	#drone.land()

else:
    print ('No exceptions are caught')