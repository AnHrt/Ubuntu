from djitellopy import Tello
import time as t

dron = Tello()
dron.connect()
print("Battery: ",dron.get_battery()) #Bateria
#print("Temp: ",dron.get_temperature()) #Temperatura

#dron.takeoff() #Despegar
#t.sleep(1)

#something.send_rc_control(y_ velocity, x_ velocity, z_ velocity, yaw_velocity)
                        # +y: derecha   / -y: izquierda
                        # +x: frente    / -x: atras
                        # +z: arriba    / -z: abajo
                        # +yaw: giro CW / -yaw: giro CWW
"""dron.send_rc_control(0,0,100,0) #Elevar el dron
t.sleep(2)
dron.send_rc_control(0,60,0,0) #Movimiento adelante
t.sleep(2)"""

#dron.land() #Aterrrizar
