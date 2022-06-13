import cv2
import numpy as np
import mediapipe as mp
from djitellopy import Tello

"""drone=Tello()
drone.connect()
print(drone.get_battery())
print(drone.get_temperature())"""

#drone.streamoff()
#camera = drone.streamon()
camera = cv2.VideoCapture(0)

Width = 640
Height = 480
Ref = 17200

#Errores en tres grados de libertad (x,y,area)
ErrorActual = np.array([0,0,0])
ErrorPrevio = np.array([0,0,0])        #Error previo

#Ganancias
Kp = np.array([0.5,0.5,0.05])         #Proporcional
Kd = np.array([0.5,0.5,0.05])         #Derivativa

velocity = (0,0,0)

mpFace = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils


def main():
    with mpFace.FaceDetection(min_detection_confidence=0.75) as face_detection:
        while True:
            re, img = camera.read()
            #img = drone.get_frame_read().frame
            img = cv2.resize(img,(Width,Height))
            img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_detection.process(img)
            img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            if results.detections:
                for face_no, detection in enumerate(results.detections):
                    mpDraw.draw_detection(img,detection)
                    if face_no==0:
                        xmin = int(detection.location_data.relative_bounding_box.xmin  * Width)
                        ymin = int(detection.location_data.relative_bounding_box.ymin  * Height)
                        xd   = int(detection.location_data.relative_bounding_box.width * Width)
                        yd   = int(detection.location_data.relative_bounding_box.height* Height)

                        print(xmin, ymin, xd, yd)

                        info = np.array([xmin+(xd/2), ymin+(yd/2), yd*xd])

                    #Controlador PD
                    ErrorPrevio = ErrorActual
                    ErrorActual = np.array([info[0]-Width/2, info[1]-Height/2, info[2]-Ref])
                    velocity = (Kp * ErrorActual) + (Kd * (ErrorActual - ErrorPrevio))
                    velocity = np.clip(velocity, -100, 100)

            else:
                velocity = np.array([0,0,0])

            #drone.send_rc_control(velocity[0],velocity[2],velocity[1],0)
            cv2.imshow("Control PD", cv2.flip(img,1))


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