import cv2 as cv
import mediapipe as mp

capture = cv.VideoCapture(0, cv.CAP_DSHOW)

width = 640
height = 480

cx0 = 0
cy0 = 0
cx4 = 0
cy4 = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 2, 0.5, 0.5)

mpDraw = mp.solutions.drawing_utils

while True:
    ret, img = capture.read()
    img = cv.resize(img,(width,height))
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    #print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            #obtaining information
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 0:
                    cv.circle(img, (cx,cy),25,(255,0,255),cv.FILLED)
                    cx0 = cx
                    cy0 = cy
                if id == 4:
                    cv.circle(img, (cx,cy),25,(255,0,255),cv.FILLED)
                    cx4 = cx
                    cy4 = cy
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        
        if(cx4 < cx0):
            cv.putText(img,"left",(10,46),cv.FONT_HERSHEY_PLAIN, 3,(255,0,255),3)
            move = 1
        elif (cx4 > cx0):
            cv.putText(img,"right",(10,46),cv.FONT_HERSHEY_PLAIN, 3,(255,0,255),3)
            move = 2
    else:
        cv.putText(img,"stop",(10,46),cv.FONT_HERSHEY_PLAIN, 3,(255,0,255),3)
        move = 0
    
    cv.imshow('webCam', img)

    if (move == 0):
        lr_speed = 0
        fb_speed = 0
        ud_speed = 0
        yaw_speed = 0
    
    if(cv.waitKey(1) == ord('q')):
        break

capture.release()
cv.destroyAllWindows()