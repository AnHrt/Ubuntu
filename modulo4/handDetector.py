import cv2
from jinja2 import pass_context
import mediapipe as mp
from djitellopy import Tello

drone=Tello()
drone.connect()
print(drone.get_battery())
print(drone.get_temperature())

drone.streamoff()
#camera = drone.streamon()

camera = cv2.VideoCapture(0)

Width = 640
Height = 480

mphand = mp.solutions.hands
hands = mphand.Hands(False, 1, 0.5, 0.5)

mpDraw = mp.solutions.drawing_utils

while True:
    re, img = camera.read()
    #img = drone.get_frame_read().frame
    img = cv2.resize(img,(Width,Height))
    iRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(iRGB)

    result = results.multi_hand_landmarks

    if result:
        for handLms in result:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h) #cardinates in pixels
                print(id,"- (", cx,",", cy,")")
                if id == 0:
                    cv2.circle(img, (cx,cy),15,(255,0,255),cv2.FILLED)
                    cx0 = cx
                    cy0 = cy
                if id == 4:
                    cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)
                    cx4 = cx
                    cy4 = cy
                if id == 5:
                    #cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)
                    cx5 = cx
                    cy5 = cy
                if id == 8:
                    cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)
                    cx8 = cx
                    cy8 = cy
                if id == 12:
                    cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)
                    cx12 = cx
                    cy12 = cy
                if id == 16:
                    cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)
                    cx16 = cx
                    cy16 = cy
                if id == 20:
                    cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)
                    cx20 = cx
                    cy20 = cy
            
            mpDraw.draw_landmarks(img, handLms, mphand.HAND_CONNECTIONS)
        
        """if (cx4 < cx0):
            cv2.putText(img,"left",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255),3)
            move = 1
        elif (cx4 > cx0):
            cv2.putText(img,"right",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255),3)
            move = 2"""
        #First down
        if (cx8>cx12 and cx12<cx4):
            #indice > dedo medio & pulgar contraido
            cv2.putText(img,"1st",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,255,0),2)
            move = 1
        #Seconf down
        elif ((cx20>cx16 and cx20>cx12) and (cx12<cx4)):
            #Meñique > anular y dedo medio & pulgar contraido 
            cv2.putText(img,"2nd",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,255,0),2)
            move = 2
        #Third down
        elif ((cx20>cx16 and cx20>cx12) and (cy4<cy5)and (cy8<cy12)):
            #Meñique > anular y dedo medio & 
            cv2.putText(img,"3rd",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,255,0),2)
            move = 3
        #Fourth down
        elif (cy4<cy8 and cy4<cy12 and cy4<cy16 and cy4<cy20):
            cv2.putText(img,"4th",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255),2)
            move = 4
        #Bad
        elif (cy4> cy20 and cy4>cy16 and cy4>cy12 and cy4>cy8 and cy4>cy0): 
            cv2.putText(img,"Bad",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,255,0),2)
            move = 5
        #Peace
        elif ((cx8-cx20 < 50) and (cx0<cx4 and cy0>cy4)):
            #pulgar contraido & dedo medio y anular juntos
            cv2.putText(img,"Peace",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,255,0),2)
            move = 6
        #FingerCrosset
        elif (cx12<cx8):
            cv2.putText(img,"FingerCrosset",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,255,0),2)
            move = 7
        #Pinky promise
        elif(cy4>cy5):
            cv2.putText(img,"Hi",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,255,0),2)
            move = 0

    else:
        cv2.putText(img,"STOP",(10,46),cv2.FONT_HERSHEY_PLAIN, 3,(255,100,255),3)
        move = 0

    cv2.imshow ("WebCam",img)

    #Movimientos
    if (takeoff_counter==0):
        drone.takeoff()
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

    if (move==3):
        lr_speed=0
        fb_speed=50
        ud_speed=0
        yaw_speed=0
        print("Forward")

    if (move==4):
        lr_speed=0
        fb_speed=-50
        ud_speed=0
        yaw_speed=0
        print("Back")

    if (move==5):
        lr_speed=0
        fb_speed=0
        ud_speed=-50
        yaw_speed=0
        print("Down")

    if (move==6):
        lr_speed=0
        fb_speed=0
        ud_speed=50
        yaw_speed=0
        print("Up")
    
    if (move==7):
        lr_speed=0
        fb_speed=0
        ud_speed=0
        yaw_speed=50
        print("Turn")

    drone.send_rc_control(lr_speed,fb_speed,ud_speed,yaw_speed)
    
    
    if (cv2.waitKey(1)==ord('q')):
        drone.streamoff()
        drone.land()
        break

camera.release()
cv2.destroyAllWindows()