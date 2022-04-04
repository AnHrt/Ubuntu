#!/usr/bin/env python 
#Define el interprete que se desea usar para ejecutar el script

#Importar librerias OK
import rospy 
from geometry_msgs.msg import Twist  #importa tipo de mensaje
from std_msgs.msg import String

class RControl(): 
    def __init__(self): 
        rospy.on_shutdown(self.stop) 

        #~~~~~~~~~~~~~~~~~~~~~~INIT PUBLISHERS~~~~~~~~~~~~~~~~~~~~~~ 
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10) 

        #~~~~~~~~~~~~~~~~~~~~~~SUBSCRIBERS~~~~~~~~~~~~~~~~~~~~~~
        rospy.Subscriber("instruction", String, self.stringCommand) 

        #~~~~~~~~~~~~~~~~~~~~~~VARIABLES~~~~~~~~~~~~~~~~~~~~~~
        self.robot = Twist()
        self.instruction = String()

        self.r = rospy.Rate(1) #1Hz 
        print("Node initialized 1hz")
        while not rospy.is_shutdown(): 
            
            self.pub.publish(self.robot)  #Publicar movimiento del robot
            self.r.sleep() 

    def stringCommand(self, instruction): 
        """ Forward / Back / Left / Right / Extra / Stop """
        if instruction.data == "Move Forward":
            self.robot.linear.x=-0.5
            self.robot.angular.z=0
        elif instruction.data == "Move Back":
            self.robot.linear.x=0.5
            self.robot.angular.z=0
        elif instruction.data == "Move Left":
            self.robot.angular.z=0.5
        elif instruction.data == "Move Right":
            self.robot.angular.z=-0.5
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
            self.robot.linear.x=0
            self.robot.angular.z=0
        else:
            print("I don't understand the instruction, TRY AGAIN")
            rospy.sleep(5)

    def stop(self): #OK 
        print("\nBye bye :)\n")

#~~~~~~~~~~~~~~~~~~~~~~PRINCIPAL~~~~~~~~~~~~~~~~~~~~~~OK
if __name__ == "__main__": 
    rospy.init_node("a_node", anonymous=True) #inicializar nodo
    # "a_node" - define el nodo
    # anonymous = True - agregar cadena de caracteres aleatoria 
    try:
        RControl() 
    except rospy.ROSInterruptException: pass