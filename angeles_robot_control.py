#!/usr/bin/env python 
#Define el interprete que se desea usar para ejecutar el script

#Importar librerias
import rospy                            #importa librerias de ROS
from geometry_msgs.msg import Twist     #importa tipo de mensaje Twist
from std_msgs.msg import String         #importa tipo de mensaje String

class RControl(): 
    def __init__(self): 
        rospy.on_shutdown(self.stop)    #

        #~~~~~~~~~~~~~~~~~~~~~~INIT PUBLISHERS~~~~~~~~~~~~~~~~~~~~~~ 
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10) 
        #cmd_vel - Topico con el que se comunica
        #Twist - tipo de mensaje que se publica
        #queue_size=10 - limite de no. de datos que recibe

        #~~~~~~~~~~~~~~~~~~~~~~SUBSCRIBERS~~~~~~~~~~~~~~~~~~~~~~
        rospy.Subscriber("instruction", String, self.stringCommand) 
        #"instruction" - topico con el que se comunica
        #String - tipo de mensaje que recibe
        #self.stringCommand - funcion callback

        #~~~~~~~~~~~~~~~~~~~~~~VARIABLES~~~~~~~~~~~~~~~~~~~~~~
        self.robot = Twist()
        self.instruction = String()

        self.r = rospy.Rate(1)          #1Hz 
        print("Node initialized 1hz")
        while not rospy.is_shutdown(): 
            
            self.pub.publish(self.robot)#Publicar movimiento del robot
            self.r.sleep()              

    def stringCommand(self, instruction): 
        # Forward / Back / Left / Right / Extra / Stop 
        if instruction.data == "Move Forward":
            self.robot.linear.x=0.5     #Movimiento lineal en el eje x
            self.robot.angular.z=0      #Anula cualquier movimiento angular en el eje z
        elif instruction.data == "Move Back":
            self.robot.linear.x=-0.5    #Movimiento lineal en el eje x
            self.robot.angular.z=0      #Anula cualquier movimiento angular en el eje z
        elif instruction.data == "Move Left":
            self.robot.angular.z=0.5    #Movimiento angular en el eje z / sentido de las manecillas de reloj
        elif instruction.data == "Move Right":
            self.robot.angular.z=-0.5   #Movimiento angular en el eje z / sentido opuesto a las manecillas de reloj
        elif instruction.data == "Move Extra": 
            #Infinito
            self.robot.linear.x=-0.5
            self.pub.publish(self.robot)
            rospy.sleep(1)
            self.robot.angular.z=1
            self.pub.publish(self.robot)
            rospy.sleep(4)
            self.robot.angular.z=0
            self.robot.linear.x=-0.5
            self.pub.publish(self.robot)
            rospy.sleep(2)
            self.robot.angular.z=-1
            self.pub.publish(self.robot)
            rospy.sleep(5)
            self.robot.angular.z=0
            self.robot.linear.x=-0.5
            self.pub.publish(self.robot)
            rospy.sleep(2)
            self.robot.linear.x=0
            self.robot.angular.z=0
            self.pub.publish(self.robot)
            rospy.sleep(1)
        elif instruction.data == "Stop":
            self.robot.linear.x=0       #Anula cualquier movimiento lineal en el eje x
            self.robot.angular.z=0      #Anula cualquier movimiento angular en el eje z
        else:
            print("I don't understand the instruction, TRY AGAIN")  #Mensaje de error
            rospy.sleep(5)

    def stop(self): 
        #Funcion ejecutada al terminar el código
        self.robot.linear.x=0           #Anula cualquier movimiento lineal en el eje x
        self.robot.angular.z=0          #Anula cualquier movimiento angular en el eje z
        self.pub.publish(self.robot)    #Publica movimiento de robot
        print("\nBye bye :)\n")

#~~~~~~~~~~~~~~~~~~~~~~PRINCIPAL~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__": 
    rospy.init_node("Angie_RControl", anonymous=True) #inicializar nodo
    # "Angie_RControl" - define el nodo
    # anonymous = True - agregar cadena de caracteres aleatoria 
    
    try: RControl() 
    except rospy.ROSInterruptException: pass