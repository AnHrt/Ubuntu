from djitellopy import Tello
import time as t
import cv2
import numpy as np

drone = Tello()
drone.connect()

drone.streamoff()
drone.streamon()

Width = 640
Height = 480

while True:
    frame_read = drone.get_frame_read().frame
    img = cv2.resize(frame_read,(Width,Height))
    cv2.imshow("Imagen original",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break
